import itertools
import re
from pickle import encode_long
from typing import List, Tuple

from dataset_model import BilingualStoryDataset


def to_list_of_sentences(dataset: BilingualStoryDataset) -> Tuple[List[str], List[str]]:
    all_english_sentences = []
    all_german_sentences = []

    def get_sentences(text: str):
        regex = r"([.!?]+)"

        # Explanation: This regex splits on punctuation marks, returning output similar
        # to "My name is Peter. I like to eat Pizza!" -> ["My name is Peter", ".", " I
        # like to eat Pizza", "!", ""], with punctuation and sentences split, and a
        # trailing empty match. We strip sentences to remove extra whitespace, filter
        # out the empty match, and put sentences and punctuation back together.

        sentences = re.split(regex, text)
        sentences = [s.strip() for s in sentences if len(s) > 0]
        pairs = zip(sentences[::2], sentences[1::2])
        sentences = [s1 + s2 for s1, s2 in pairs]

        return sentences

    for i, story in enumerate(dataset.stories):
        # Get English sentences
        english_text = story.english.text
        english_sentences = get_sentences(english_text)

        # Get German sentences
        german_text = story.german.text
        german_sentences = get_sentences(german_text)

        # Check for sentence mismatch
        if len(english_sentences) != len(german_sentences):
            print(f"[{i}] Sentence mismatch, excluding story")

        # Store
        all_english_sentences.extend(english_sentences)
        all_german_sentences.extend(german_sentences)

    return all_english_sentences, all_german_sentences


def main():
    with open("dataset/simple-bilingual-stories.json", mode="r") as f:
        dataset = BilingualStoryDataset.model_validate_json(f.read())

    english_sentences, german_sentences = to_list_of_sentences(dataset)

    with open("dataset/simple-bilingual-stories-eng-sentences.txt", mode="w") as f:
        f.write("\n".join(english_sentences))
    with open("dataset/simple-bilingual-stories-ger-sentences.txt", mode="w") as f:
        f.write("\n".join(german_sentences))


if __name__ == "__main__":
    main()