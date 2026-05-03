# Word Frequency Analysis Tool

A tool for processing texts into word webs - simple, undirected, unweighted graphs which connect words (and interpunction) based on co-occurrence. Useful in network analysis.

## Structure

```text
.
├── main.py
├── scripts/
│   ├── utils.py
│   ├── Book.py
│   └── Wordweb.py
├─── text_files/
│   └── ...
└── books.yaml
```

* `main.py` — entry point of the application, it reads books.yaml and does stuff based on given action word (argument)
* `books.yaml` — conf file describing each source text
* `text_files/` — directory containing all source texts
* `utils.py` — helper functions
* `scripts/Book.py` — handles book/text processing
* `scripts/Wordweb.py` — handles construction of the graphs and outputting their characteristics

## Requirements

* Python 3.x

Install dependencies if needed:

```bash
pip install -r requirements.txt
```

## Usage

Run the program using:

```bash
python main.py <action>
```

Example:

```bash
python main.py plot_degree_distribution
```

If no action is provided, or an invalid action is used, the program will display the list of available actions automatically.

## Available Actions

The available actions include:

print_info - prints all basic characteristics of the graphs with scaling exponents in two regime degree distribution
number_of_words - prints number of words per source text
plot_degree_distribution - plots degree -> probability of degree graph with two regression lines (small and large degrees)
draw_graph - draws cool (but kind of irrelevant) graph using spring layout

## Text Sources

Some text files included in this project originate from Project Gutenberg.

* Original works are in the public domain
* Project Gutenberg headers/licenses are retained in the source files where applicable

## Purpose

This project was created for my bachelor thesis. 

## License

This project was developed as part of a bachelor's thesis at Univerzita Komenského v Bratislave.
Copyright ownership may be subject to university policies.

is this good?
