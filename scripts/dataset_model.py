from typing import List

from pydantic import BaseModel


class Story(BaseModel):
    title: str
    text: str


class BilingualStory(BaseModel):
    english: Story
    german: Story


class BilingualStoryDataset(BaseModel):
    stories: List[BilingualStory]
