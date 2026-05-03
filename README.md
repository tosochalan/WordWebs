\# Word Frequency Analysis Tool



A tool for processing texts into word webs - simple, unoriented, unweighted graphs which connect words (and punctuation) based on co-occurrence. Useful in network analysis.



\## Structure



```text

.

├── main.py

├── scripts/

│   ├── utils.py

│   ├── Book.py

│   └── Wordweb.py

├─── text\_files/

│   └── ...

└── books.yaml

```



\* `main.py` — entry point of the application, reads books.yaml and does stuff based on given action word

\* `books.yaml` — configuration file describing each source text

\* `text\_files/` — directory containing all source texts

\* `utils.py` — helper functions

\* `scripts/Book.py` — handles book/text processing

\* `scripts/Wordweb.py` — handles construction of the graphs and outputting their characteristics



\## Requirements



\* Python 3.x



Install dependencies if needed:



```bash

pip install -r requirements.txt

```



\## Usage



Run the program using:



```bash

python main.py <action>

```



Example:



```bash

python main.py plot\_degree\_distribution

```



If no action is provided, or an invalid action is used, the program will display the list of available actions automatically.



\## Available Actions



\* `print\_info` — prints basic graph characteristics and scaling exponents for two-regime degree distributions

\* `number\_of\_words` — prints the number of words per source text

\* `plot\_degree\_distribution` — plots degree probability distributions with regression lines for small and large degrees

\* `draw\_graph` — draws a visual representation of the graph using a spring layout



\## Text Sources



Some text files included in this project originate from Project Gutenberg.



\* Original works are in the public domain

\* Project Gutenberg headers/licenses are retained in the source files where applicable



\## Purpose



This project was created for my bachelor thesis. 



\## License



This project was developed as part of a bachelor's thesis at Univerzita Komenského v Bratislave.

Copyright ownership may be subject to university policies.

