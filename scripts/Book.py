from . import utils
import re


class Book:
    def __init__(self, title, file_name, start_line, end_line):
        """
        Docstring for __init__

        :param self: ...
        :param title: Title of the book
        :param file_name: File name containing the book text
        :param start_line: Starting line of the core text (to skip table of contents, etc.) indexed from 1
        :param end_line: Ending line of the core text (to skip appendices, etc.)
        """

        self.title = title
        self.file_name = file_name
        self.start_line = start_line
        self.end_line = end_line

    def get_text(self) -> str:
        """
        Returns the text of the book between start_line and end_line.

        :param self: ...
        :return: Text of the book
        :rtype: str
        """

        file = open(self.file_name, encoding='utf-8')
        text = "".join(file.readlines()[self.start_line - 1:self.end_line])
        file.close()
        return text

    def get_number_of_words(self) -> int:
        """
        Returns the number of words in the book text.

        :param self: ...
        :return: Number of words in the book
        :rtype: int
        """

        text = self.get_text()
        words = text.split()
        return len(words)

    def get_tokens(self) -> list:
        """
        Returns a list of tokens in the book text.

        :param self: ...
        :return: List of tokens in the book
        :rtype: list
        """

        text = self.get_text()
        words = re.split(r"[\s\-\u2013\u2014]+", text)  # too many words connected with dashes like: 'blood-stain', 'there—there—at'
        tokens = []
        for word in words:
            stripped_word = utils.strip_word(word)[0]
            if stripped_word:
                tokens.append(stripped_word)
        return tokens

    def get_tokens_punctuation(self) -> list:
        """
        Returns a list of tokens in the book text, including interpunction as separate tokens.

        :param self: ...
        :return: List of tokens in the book
        :rtype: list
        """

        text = self.get_text()
        words = re.split(r"[\s\-\u2013\u2014]+", text)
        tokens = []
        for word in words:
            for subword in utils.split_word(word):
                if subword:
                    tokens.append(subword)
        return tokens


if __name__ == "__main__":
    ot = Book("Oliver Twist", "text_files/oliver_twist.txt", 141, 18835)
    bh = Book("Bleak House", "text_files/bleak_house.txt", 208, 39868)
    omf = Book("Our Mutual Friend", "text_files/our_mutual_friend.txt", 126, 38681)

    text = ot.get_text()
    print(f"Text of {ot.title}:\n{text[:100]}...\n")
    print(f"\n{text[-100:]}\n")

    for book in (ot, bh, omf):
        print(f"{book.title} has {book.get_number_of_words()} words.")
