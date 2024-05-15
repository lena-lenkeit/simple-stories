# Simple Stories
A dataset of 10k short and very simple bilingual (English/German) stories sampled from Claude 3 Haiku. This dataset is part of my research project on Unsupervised Machine Translation. Inspired by TinyStories, the key difference here is the bilingual nature of the stories. The repository also includes the scripts and prompts used for sampling, allowing for the creation of larger or stylistically different datasets.

## License
The dataset and scripts are available for non-commercial research purposes only. Please ensure compliance with the [Anthropic Usage Policy](https://www.anthropic.com/legal/aup) when using this dataset or running the associated scripts.

## Format
Multiple formats of the dataset are provided:

### Single large JSON dictionary (`.json`)
A list of dictionaries containing each bilingual story pair and title, directly parseable via JSON. A Pydantic model is also included for easy loading.

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
        }
    ]
}
```

### Line-separated JSON dictionaries (`.jsonl`)
Similar to the above, but each dictionary is on a new line, making it useful for various data loading strategies.

``` json
{"english":{"title":"The Adventures of Ziggy the Zany Zebra","text":"Ziggy the zebra was a very silly animal. He loved to run around and play all day. Ziggy had black and white stripes that made him look extra zany. He would jump and twirl, making all his friends laugh. Ziggy's favorite thing to do was to race the other animals in the meadow. He always won because he was the fastest and the funniest zebra around!"},"german":{"title":"Die Abenteuer von Ziggy, dem verrückten Zebra","text":"Ziggy, das Zebra, war ein sehr silliges Tier. Er liebte es, den ganzen Tag herumzurennen und zu spielen. Ziggys schwarze und weiße Streifen machten ihn extra verrückt aussehend. Er würde springen und sich drehen, sodass all seine Freunde lachten. Ziggys Lieblingsaktivität war es, mit den anderen Tieren auf der Wiese um die Wette zu rennen. Er gewann immer, denn er war das schnellste und lustigste Zebra weit und breit!"}}
{"english":{"title":"Daisy's Delightful Day at the Dandelion Patch","text":"Daisy the dog loved to play in the dandelion patch. She would run through the yellow flowers, chasing butterflies and sniffing the sweet scents. Daisy would pick up the fluffy dandelion seeds in her mouth and blow them into the air, watching them float away. She would roll in the soft grass and bark with joy. Daisy had the best day ever in the dandelion patch!"},"german":{"title":"Daisys wunderbarer Tag auf der Löwenzahnwiese","text":"Die Hündin Daisy liebte es, auf der Löwenzahnwiese zu spielen. Sie rannte durch die gelben Blumen, jagte Schmetterlinge und schnupperte an den süßen Düften. Daisy nahm die flauschigen Löwenzahnsamen in den Mund und blies sie in die Luft, wo sie davonschwebten. Sie wälzte sich im weichen Gras und bellte vor Freude. Daisy hatte den besten Tag überhaupt auf der Löwenzahnwiese!"}}
```

### Individual sentences (`.txt`)
Two text files, one for the English stories and one for the German stories. Each line in the files corresponds to the same story sentence in both languages. A regex `([.!?]+)` is used to split the sentences.

**English**
``` txt
Ziggy the zebra was a very silly animal.
He loved to run around and play all day.
Ziggy had black and white stripes that made him look extra zany.
```

**German**
``` txt
Ziggy, das Zebra, war ein sehr silliges Tier.
Er liebte es, den ganzen Tag herumzurennen und zu spielen.
Ziggys schwarze und weiße Streifen machten ihn extra verrückt aussehend.
```

## Sampling Strategy
Stories are generated in two stages. First, a prompt generates 10 titles for simple children's stories. Each title is then used to sample an entire story. The stories are initially sampled in English, followed by German within the same query.

## Observations
(Note: I'm fluent in both English and German)
- **Quality**
  - Translations of titles into German tend to be poor, especially the articles. I wouldn't recommend training on them.
  - English texts of the stories look fine. German translations are mostly correct, although Claude 3 Haiku sometimes incorrectly translates a few words ("silly animal" -> "silliges Tier," but it should be "albernes Tier" or similar). Articles in German also seem problematic at times.

- **Patterns**
  - Claude 3 Haiku seems to be obsessed with alliterations both in story titles and texts.
  - Haiku has a strong preference for certain titles. The three most common English titles are "The Curious Caterpillar" (434 times), "The Friendly Frog" (140 times), and "The Helpful Hedgehog" (140 times).
  - Haiku tends to favor stories involving animals.

## Dataset Statistics
- Number of stories: 10,000
- Avg. words per story: 135
- Avg. sentences per story: 15

Run the statistics script to see more.
