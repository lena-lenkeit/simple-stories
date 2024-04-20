import re
from collections import Counter

from dataset_model import BilingualStory, BilingualStoryDataset


def analyze_dataset(dataset: BilingualStoryDataset):
    num_stories = len(dataset.stories)
    print(f"Number of stories: {num_stories}")

    stories_num_words = []
    stories_num_sentences = []

    word_counter = Counter()
    title_counter = Counter()

    word_regex = r"\b\w+\b"
    sentence_regex = r"[.!?]+"

    for story in dataset.stories:
        # Extract word and sentence counts for English story
        english_text = story.english.text
        english_words = re.findall(word_regex, english_text)
        english_sentences = re.split(sentence_regex, english_text)

        stories_num_words.append(len(english_words))
        stories_num_sentences.append(len(english_sentences))

        word_counter.update(english_words)

        # Extract word and sentence counts for German story
        german_text = story.german.text
        german_words = re.findall(word_regex, german_text)
        german_sentences = re.split(sentence_regex, german_text)

        stories_num_words.append(len(german_words))
        stories_num_sentences.append(len(german_sentences))

        word_counter.update(german_words)

        if len(english_sentences) != len(german_sentences):
            print(f"Mismatch between english and german sentences")

        # Collect titles
        title_counter.update([story.english.title])
        title_counter.update([story.german.title])

    # Calculate average word count per story
    avg_word_count = sum(stories_num_words) / num_stories
    print(f"Average word count per story: {avg_word_count:.2f}")

    # Calculate average sentence count per story
    avg_sentence_count = sum(stories_num_sentences) / num_stories
    print(f"Average sentence count per story: {avg_sentence_count:.2f}")

    # Count duplicate titles
    duplicate_titles = [
        (title, count) for title, count in title_counter.items() if count > 1
    ]
    print(f"Number of duplicate titles: {len(duplicate_titles)}")
    print(
        "Duplicate titles:", sorted(duplicate_titles, key=lambda x: x[1], reverse=True)
    )

    # Count occurrences of individual words
    print("Top 100 most common words:")
    for word, count in word_counter.most_common(100):
        print(f"{word}: {count}")


def main():
    with open("dataset/simple-bilingual-stories.json", mode="r") as f:
        analyze_dataset(BilingualStoryDataset.model_validate_json(f.read()))


if __name__ == "__main__":
    main()
