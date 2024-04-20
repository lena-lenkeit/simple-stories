import logging
import signal
import sys
import time
import xml.etree.ElementTree as ET
from typing import Callable, List, TypeVar

from anthropic import Anthropic
from pydantic import BaseModel
from tqdm.auto import trange

logger = logging.getLogger(__name__)


class Story(BaseModel):
    title: str
    text: str


class BilingualStory(BaseModel):
    english: Story
    german: Story


class BilingualStoryDataset(BaseModel):
    stories: List[BilingualStory]


def sample_titles(client: Anthropic, prompt: str, num_titles: int = 10) -> List[str]:
    # Query
    message = client.messages.create(
        max_tokens=1024,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": prompt.format(num_titles=num_titles),
            }
        ],
        model="claude-3-haiku-20240307",
    )

    # Parse
    title_string = message.content[0].text
    xml_string = f"<root>{title_string}</root>"
    root = ET.fromstring(xml_string)
    titles = [title.text.strip() for title in root.findall("title")]

    if len(titles) != num_titles:
        raise ValueError("Length mismatch between requested and received title list")

    return titles


def sample_story(client: Anthropic, prompt: str, title: str) -> BilingualStory:
    # Query
    message = client.messages.create(
        max_tokens=1024,
        temperature=1,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": title,
            }
        ],
        model="claude-3-haiku-20240307",
    )

    # Parse
    story_string = message.content[0].text
    xml_string = f"<root>{story_string}</root>"
    root = ET.fromstring(xml_string)

    english_story = root.find("english")
    german_story = root.find("german")

    return BilingualStory(
        english=Story(
            title=english_story.find("title").text.strip(),
            text=english_story.find("text").text.strip(),
        ),
        german=Story(
            title=german_story.find("title").text.strip(),
            text=german_story.find("text").text.strip(),
        ),
    )


T = TypeVar("T")


def query_with_backoff(
    fn: Callable[..., T], fn_kwargs: dict, backoff_init: float, backoff_factor: float
) -> T:
    backoff_value = backoff_init
    num_attempts = 1
    while True:
        logger.log(
            logging.INFO,
            f"Querying {fn} with kwargs {fn_kwargs} (Attempt {num_attempts})",
        )

        try:
            return fn(**fn_kwargs)
        except Exception as e:
            logger.log(logging.WARN, f"Query failed with exception: {e}")
            time.sleep(backoff_value)
            backoff_value *= backoff_factor
            num_attempts += 1


def signal_handler(sig, frame):
    signal_handler.num_interrupts += 1
    if signal_handler.num_interrupts > 1:
        sys.exit(-1)

    logger.log(
        logging.WARN, "Received SIGINT, gracefully exiting (Send again to force exit)"
    )


signal_handler.num_interrupts = 0


def main():
    # Directories and Files
    key_file = "keys/anthropic.txt"
    title_prompt_file = "prompts/generate_titles.txt"
    story_prompt_file = "prompts/generate_story.txt"
    dataset_file = "dataset/simple-bilingual-stories.json"

    # Sizes
    num_stories = 100
    num_titles = 10

    # Saving
    save_interval = 10

    # Register graceful SIGINT handler
    signal.signal(signal.SIGINT, signal_handler)

    # Log to file
    logging.basicConfig(filename="logger.log", encoding="utf-8", level=logging.INFO)

    # Set-up Anthropic client
    with open(key_file, mode="r") as f:
        client = Anthropic(api_key=f.read())

    # Get prompts
    with open(title_prompt_file, mode="r") as f:
        title_prompt = f.read()

    with open(story_prompt_file, mode="r") as f:
        story_prompt = f.read()

    # Try to load or create a new dataset
    try:
        with open(dataset_file, mode="r") as f:
            story_dataset = BilingualStoryDataset.model_validate_json(f.read())
    except OSError:
        logger.log(logging.INFO, "No existing dataset found, creating a new one")
        story_dataset = BilingualStoryDataset(stories=[])
    except ValueError:
        logger.log(logging.ERROR, "Could not validate existing dataset! Exiting")
        sys.exit(-1)

    def save_dataset():
        logger.log(
            logging.INFO, f"Saving dataset with {len(story_dataset.stories)} stories"
        )
        with open(dataset_file, mode="w") as f:
            f.write(story_dataset.model_dump_json(indent=4))

    # Query new stories
    title_queue = []
    for story_id in trange(len(story_dataset.stories), num_stories):
        # Query new titles, if none left
        if len(title_queue) == 0:
            logger.log(
                logging.INFO, f"Title queue empty, querying {num_titles} new titles"
            )
            title_queue.extend(sample_titles(client, title_prompt, num_titles))

        title = title_queue.pop(0)
        logger.log(
            logging.INFO,
            f"Querying new story with title {title} ({story_id + 1} of {num_stories})",
        )

        # Query story
        story = sample_story(client, story_prompt, title)
        story_dataset.stories.append(story)

        # Handle saving and graceful exiting
        do_save = len(story_dataset.stories) % save_interval == 0
        do_exit = signal_handler.num_interrupts > 0

        if do_save:
            save_dataset()
        if do_exit:
            break

    save_dataset()


if __name__ == "__main__":
    main()
