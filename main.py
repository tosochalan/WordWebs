from scripts.Wordweb import Wordweb
from scripts.Book import Book
import yaml
import sys


def load_books(file_path: str) -> list[Book]:
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return [Book(**book_data) for book_data in data.get('books', [])]
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")
        return []


def print_info(word_web, word_web_no_punctuation) -> None:
    word_web.print_info()
    word_web_no_punctuation.print_info()

    print("additional nodes:", word_web.nodes_difference(word_web_no_punctuation))


def number_of_words(book) -> None:
    print(book.title, book.get_number_of_words())


def plot_degree_distribution(word_web, word_web_no_punctuation) -> None:
    word_web.plot_multi_regime_degree_distribution()
    word_web_no_punctuation.plot_multi_regime_degree_distribution()


if __name__ == '__main__':
    available_commands = ['print_info', 'number_of_words', 'plot_degree_distribution', 'draw_graph']
    command = ''
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command not in available_commands:
        commands_text = "".join(["    " + command + "\n" for command in available_commands])
        print(f"Available commands:\n{commands_text}")
        exit(1)

    books = load_books('books.yaml')

    for book in books:
        word_web = Wordweb(book=book, num_of_links_from_new_word=2, punctuation=True)
        word_web_no_punctuation = Wordweb(book=book, num_of_links_from_new_word=2, punctuation=False)

        if command == 'print_info':
            print_info(word_web, word_web_no_punctuation)

        elif command == 'number_of_words':
            number_of_words(book)

        elif command == 'plot_degree_distribution':
            plot_degree_distribution(word_web, word_web_no_punctuation)

        elif command == 'draw_graph':
            word_web.draw_graph()
