# Simple Stories
A dataset of 10k short and very simple bilingual (English / German) stories sampled from Claude 3 Haiku, which I'm using as part of another research project on Unsupervised Machine Translation. Inspired by TinyStories, but with the key difference of having bilingual stories. Also includes the scripts and prompts used for sampling, so you could sample a larger dataset in a different style for example.

## License
I'm making the dataset and the scripts available for non-commercial research purposes only. Please make sure to comply with the Anthropic Usage Policy when using this dataset or running the associated scripts.

## Format
I provide multiple different formats for the dataset.

### Single large json dictionary (`.json`)

A list of dictionaries containing each bilingual story pair and title, directly parseable via json. I also include a Pydantic model for this format for easy loading.

``` json
{
    "stories": [
        {
            "english": {
                "title": "The Adventures of Ziggy the Zany Zebra",
                "text": "Ziggy the zebra was a very silly animal. He loved to run around and play all day. Ziggy had black and white stripes that made him look extra zany. He would jump and twirl, making all his friends laugh. Ziggy's favorite thing to do was to race the other animals in the meadow. He always won because he was the fastest and the funniest zebra around!"
            },
            "german": {
                "title": "Die Abenteuer von Ziggy, dem verrückten Zebra",
                "text": "Ziggy, das Zebra, war ein sehr silliges Tier. Er liebte es, den ganzen Tag herumzurennen und zu spielen. Ziggys schwarze und weiße Streifen machten ihn extra verrückt aussehend. Er würde springen und sich drehen, sodass all seine Freunde lachten. Ziggys Lieblingsaktivität war es, mit den anderen Tieren auf der Wiese um die Wette zu rennen. Er gewann immer, denn er war das schnellste und lustigste Zebra weit und breit!"
            }
        },
        {
            "english": {
                "title": "Daisy's Delightful Day at the Dandelion Patch",
                "text": "Daisy the dog loved to play in the dandelion patch. She would run through the yellow flowers, chasing butterflies and sniffing the sweet scents. Daisy would pick up the fluffy dandelion seeds in her mouth and blow them into the air, watching them float away. She would roll in the soft grass and bark with joy. Daisy had the best day ever in the dandelion patch!"
            },
            "german": {
                "title": "Daisys wunderbarer Tag auf der Löwenzahnwiese",
                "text": "Die Hündin Daisy liebte es, auf der Löwenzahnwiese zu spielen. Sie rannte durch die gelben Blumen, jagte Schmetterlinge und schnupperte an den süßen Düften. Daisy nahm die flauschigen Löwenzahnsamen in den Mund und blies sie in die Luft, wo sie davonschwebten. Sie wälzte sich im weichen Gras und bellte vor Freude. Daisy hatte den besten Tag überhaupt auf der Löwenzahnwiese!"
            }
        },
```

### Line-separated json dictionaries (`.jsonl`)

Similar to above, but each dictionary individually on a newline. Useful for some data loading strategies.

``` json
{"english":{"title":"The Adventures of Ziggy the Zany Zebra","text":"Ziggy the zebra was a very silly animal. He loved to run around and play all day. Ziggy had black and white stripes that made him look extra zany. He would jump and twirl, making all his friends laugh. Ziggy's favorite thing to do was to race the other animals in the meadow. He always won because he was the fastest and the funniest zebra around!"},"german":{"title":"Die Abenteuer von Ziggy, dem verrückten Zebra","text":"Ziggy, das Zebra, war ein sehr silliges Tier. Er liebte es, den ganzen Tag herumzurennen und zu spielen. Ziggys schwarze und weiße Streifen machten ihn extra verrückt aussehend. Er würde springen und sich drehen, sodass all seine Freunde lachten. Ziggys Lieblingsaktivität war es, mit den anderen Tieren auf der Wiese um die Wette zu rennen. Er gewann immer, denn er war das schnellste und lustigste Zebra weit und breit!"}}
{"english":{"title":"Daisy's Delightful Day at the Dandelion Patch","text":"Daisy the dog loved to play in the dandelion patch. She would run through the yellow flowers, chasing butterflies and sniffing the sweet scents. Daisy would pick up the fluffy dandelion seeds in her mouth and blow them into the air, watching them float away. She would roll in the soft grass and bark with joy. Daisy had the best day ever in the dandelion patch!"},"german":{"title":"Daisys wunderbarer Tag auf der Löwenzahnwiese","text":"Die Hündin Daisy liebte es, auf der Löwenzahnwiese zu spielen. Sie rannte durch die gelben Blumen, jagte Schmetterlinge und schnupperte an den süßen Düften. Daisy nahm die flauschigen Löwenzahnsamen in den Mund und blies sie in die Luft, wo sie davonschwebten. Sie wälzte sich im weichen Gras und bellte vor Freude. Daisy hatte den besten Tag überhaupt auf der Löwenzahnwiese!"}}
```

### Individual sentences (`.txt`)

Two text files, one for the English, and one for the German stories. There is a one-to-one correspondence between line numbers of the files, i.e. line X in both files contains the same text, just either in English or German. I use this regex `([.!?]+)` to split sentences.

English
``` txt
Ziggy the zebra was a very silly animal.
He loved to run around and play all day.
Ziggy had black and white stripes that made him look extra zany.
```

German
``` txt
Ziggy, das Zebra, war ein sehr silliges Tier.
Er liebte es, den ganzen Tag herumzurennen und zu spielen.
Ziggys schwarze und weiße Streifen machten ihn extra verrückt aussehend.
```

## Sampling strategy
I sample stories in two stages. First, a prompt is used to generate 10 titles for simple children's stories. Then, each title is used in independent queries to sample the actual story. Each story is sampled in English first and then in German within the same query.

## Observations
(Note: I'm fluent in both English and German)
- Quality
  - Translations of titles into German tend to be bad for some reason, especially the articles. I wouldn't recommend training on them.
  - English texts of stories look fine to me. German translations are mostly correct, though Claude 3 Haiku seems to sometimes incorrectly translate a few words ("silly animal" -> "silliges Tier", but should be -> "albernes Tier" or similar). Again, articles seem to be messed up sometimes as well.
  - Most stories have the same number of sentences. I filter out mismatched stories for the sentence-level datasets.
  
- Patterns
  - Claude 3 Haiku seems to be obsessed with alliterations, both in story titles and the text of stories.
  - Claude 3 Haiku has a strong preference for some titles. The three most common English titles for example are "The Curious Caterpillar" (434 times), "The Friendly Frog" (140 times) and "The Helpful Hedgehog" (140 times).
  - Claude 3 Haiku tends to prefer stories involving animals.


## Dataset statistics
- Number of stories: 10,000
- Avg. words per story: 135
- Avg. sentences per story: 15

Run the statistics script to see more statistics.
