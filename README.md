# Lesson 22 study package - My Daughter Jane and the Drift Bottle

A multimodal study pack built from one handout: a 10-page New Concept English (Book 2)
Lesson 22 walkthrough (vocabulary, text, pronunciation, grammar and writing).
Everything in this folder is **English only**.

## Lesson facts

| Item | Value |
| --- | --- |
| Lesson | Lesson 22 |
| Title used here | My Daughter Jane and the Drift Bottle |
| Title note | The handout gives no lesson title; this one is a summary of the text. The textbook's usual title "A glass envelope" does not appear in the handout. |
| Source | `Lesson22(1).pdf` (New Concept AI edition, course detail sheet 3, 10 pages) |
| Source path | `/Users/jacklei/Documents/NCE2/Lesson22(1).pdf` |
| Target level | Senior high school to CET-4 |
| Page references | The PDF footers `1/10`-`10/10`, written here as `p1`-`p10` |
| Package language | English only |

### Language note

The handout itself is Chinese-medium. In this English-only edition its Chinese
explanations and translations are rendered as **plain-English glosses**, and every
quoted English sentence is kept exactly as the handout prints it. Wherever the
handout is silent - the lesson title, sentence stress, intonation - the files say
`not given in the handout` rather than filling the gap with a guess.

## What is in the folder

| File | What it is | How to open it |
| --- | --- | --- |
| `index.html` | The whole lesson as one offline page: Overview, Vocabulary, Grammar, Text, Pronunciation, Practice (interactive), Writing | Double-click it. No server, no internet, no external files |
| `data.json` | The single source of truth: 4 vocabulary entries, 8 grammar points, the 7 sentences with timeline and teaching points, pronunciation marks, writing model, and 45 interactive practice items (including 7 guided imitation-writing frames) | Any text editor or JSON viewer |
| `mindmap.mmd` | Mermaid mind map: vocabulary, grammar, text, pronunciation, writing, practice | Mermaid Live Editor, or any Markdown tool with Mermaid support |
| `concept-map.mmd` | Mermaid concept map: dream pattern network, confusables, the verb + preposition network, tense contrast, the text's logic chain | Same as above |
| `prepositions.svg` | Image schemas for **in / on / from / of**, each with its core idea, a diagram, two quoted examples and the extended patterns | Any browser, or any image viewer that reads SVG |
| `timeline.svg` | The five-tense timeline of the text with a colour legend, page references and the handout's own note for each step | Any browser |
| `anki.csv` | 40 Anki cards, UTF-8, columns `Front,Back,Tags,Examples,Image` | Anki: File > Import |
| `README.md` | This file | - |
| `_tools/build.py` | Regenerates `index.html` and `anki.csv` from `data.json` | `python3 _tools/build.py` |
| `_tools/assets/` | The handout's two pronunciation images (used by the build script) | Any image viewer |

## Colour conventions

Two palettes are used, and they are never mixed:

* **Tense colours** - only in `timeline.svg` and in the tense tags on the Text tab:
  past continuous `#2563eb` (blue), past simple `#16a34a` (green),
  present perfect `#ea580c` (orange), present simple `#7c3aed` (purple),
  future simple `#dc2626` (red).
* **Preposition colours** - only in `prepositions.svg`:
  in `#2563eb` (blue), on `#16a34a` (green), from `#ea580c` (orange), of `#7c3aed` (purple).

The Grammar tab prints a small coloured chip next to each grammar point so you can see
which preposition colour it belongs to.

## Using index.html

* Seven tabs across the top: **Overview, Vocabulary, Grammar, Text, Pronunciation, Practice, Writing**.
* Deep links work: `index.html#vocab`, `#grammar`, `#text`, `#pron`, `#ex`, `#writing`.
* The Overview tab has six study steps with checkboxes; your ticks are saved in the
  browser's `localStorage` and the counter in the header shows how far you have got.
* The Practice tab is fully interactive: click an option (multiple choice), type the missing
  word (gap fill), choose True or False, click the given words in the right order (word order),
  click a left item then its partner (matching), and fill the imitation-writing frames one
  sentence at a time. Every item gives instant feedback with the reason, the score is kept in
  your browser, and **Reset score** / **Show every answer** are always available.
* The Grammar and Text tabs embed the two SVG diagrams; the Pronunciation tab embeds the
  handout's original marked-up images. On a phone the diagrams scroll sideways: the wide
  layout is intentional, so that the text inside them stays readable.
* Nothing is loaded from the internet. The page works offline, including on a phone if you
  copy the single file across.

## Importing anki.csv into Anki

1. In Anki: **File > Import**, choose `anki.csv`.
2. Set **Field separator** to `Comma` and **Allow HTML in fields** as you prefer (the file
   contains no HTML).
3. Map the five columns in this order: `Front`, `Back`, `Tags`, `Examples`, `Image`.
   The first row is a header row, so tick **Field names are in the first line** if your
   version offers the option.
4. Choose the note type. `Basic` fits directly; the `Examples` and `Image` columns can be
   appended to the answer template if you want them on the back.
5. Tags are separated by spaces (not commas) and look like
   `Lesson22 vocab preposition` - Anki splits them correctly on spaces.
6. The `Image` column names `prepositions.svg` or `timeline.svg` on the cards that belong to
   a diagram. Copy those two SVG files into your Anki `collection.media` folder if you want
   the pictures to appear; otherwise leave the column unused and Anki simply shows nothing.
7. The deck has 40 cards: vocabulary and patterns, the four prepositions, the five tenses of
   the text, text and writing points, and pronunciation.

## Reviewing the two SVG diagrams

* `prepositions.svg` - cover the two example sentences in each panel and say them from the
  picture: the container for **in**, the contact surface for **on**, the arrow leaving the
  start point for **from**, the two linked nodes for **of**. Then recall the extended
  patterns printed at the bottom of each panel.
* `timeline.svg` - read the timeline top to bottom and say the tense out loud before you read
  the label. Cover the right-hand notes and reproduce the handout's point for each step:
  background before `and`, the point after `and`, the point after `but`, `now` for the
  present simple, the effect on the present for the present perfect, and `will` for the
  future.

## Suggested study routine

1. **Look** - open the diagrams first (`prepositions.svg`, `timeline.svg`) and match each
   colour to its idea.
2. **Read** - work through the Vocabulary tab aloud, one pattern at a time, checking the page
   reference so you know where it comes from.
3. **Practise** - work through the Practice tab: 9 multiple-choice, 12 gap-fill, 9 true/false, 6 word-order, 3 matching and 7 guided-writing frames. Answers are checked in the browser and your score is saved; for every mistake, go back to the page named in
   the item and re-read that example.
4. **Write** - use the seven-step template on the Writing tab with a new topic of your own.
5. **Retell** - tell the whole story in five sentences, keeping the tense chain in order.
6. **Review** - import `anki.csv` and work through the 40 cards; pair the diagram cards with
   the SVG files.

## Rebuilding the package

```bash
cd <this folder>
python3 _tools/build.py     # rewrites index.html and anki.csv from data.json
```

The script needs, in this folder: `data.json`, `prepositions.svg`, `timeline.svg` and the two
images in `_tools/assets/`. Nothing else is required; there are no third-party packages.

## Fidelity and limits

* Every example sentence in this package is quoted from the handout, p1-p10; none was invented.
* Page numbers follow the PDF's own footers, so any claim in `data.json` can be checked against
  the page it names.
* Core and extended meanings are kept in separate fields for each word.
* Part 3 Pronunciation (`p7`) has **no text at all** in the PDF: its content is two images.
  The Pronunciation tab therefore transcribes those marks into searchable text and embeds the
  original images, so you can always compare the transcription with the source.
* The handout marks no sentence stress and no intonation, so this package states that instead
  of inventing a pattern.
