import pytest
from scripts.Book import Book

@pytest.fixture
def test_book(tmp_path):
    file = tmp_path / "test_book.txt"
    file.write_text("This is the introduction, skip me.\nThis is the multiple line core.\nDon\'t skip me\nAnd some words at the tail.\nskip")
    book = Book("Test Book", str(file), 2, 3)
    return book


@pytest.fixture
def test_book_dashes(tmp_path):
    file = tmp_path / "test_book.txt"
    file.write_text("This is the introduction, skip me.\nThis is the multiple line core.\nelbow-chair all—as flat-browed\nAnd some words at the tail.\nskip", encoding="utf-8")
    book = Book("Test Book", str(file), 2, 3)
    return book

def test_get_text(test_book):
    text = test_book.get_text()
    assert text == "This is the multiple line core.\nDon't skip me\n"

def test_get_number_of_words(test_book):
    assert test_book.get_number_of_words() == 9

def test_get_tokens(test_book):
    assert test_book.get_tokens() == ["this", "is", "the", "multiple", "line", "core", "don't", "skip", "me"]

def test_get_tokens_dashes(test_book_dashes):
    assert test_book_dashes.get_tokens() == ["this", "is", "the", "multiple", "line", "core", "elbow", "chair", "all", "as", "flat", "browed"]

def test_get_tokens_punctuation(test_book):
    assert test_book.get_tokens_punctuation() == ["this", "is", "the", "multiple", "line", "core", ".", "don't", "skip", "me"]
