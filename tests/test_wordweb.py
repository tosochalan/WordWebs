import pytest
from scripts.Wordweb import Wordweb
from scripts.Book import Book

@pytest.fixture
def test_book(tmp_path):
    file = tmp_path / "test_book.txt"
    file.write_text("This is the introduction, skip me.\nJohn likes dog a lot.\nDog likes to sleep.\nAnd some words at the tail.\nskip")
    book = Book("Test Book", str(file), 2, 3)
    return book

def test_wordweb_construction(test_book):
    w = Wordweb(book=test_book, num_of_links_from_new_word=1)
    assert w.G.number_of_nodes() == 7
    assert w.G.number_of_edges() == 7

    nodes = ["john", "likes", "dog", "a", "lot", "to", "sleep"]
    for node in nodes:
        assert node in w.G.nodes
    
    edges = [("john", "likes"), ("likes", "dog"), ("likes", "to"), ("dog", "a"), ("dog", "lot"), ("a", "lot"), ("to", "sleep")]
    for edge in edges:
        assert w.G.has_edge(*edge)
    
def test_wordweb_construction_multiple_links(test_book):
    w = Wordweb(book=test_book, num_of_links_from_new_word=2)
    assert w.G.number_of_nodes() == 7
    assert w.G.number_of_edges() == 12

    nodes = ["john", "likes", "dog", "a", "lot", "to", "sleep"]
    for node in nodes:
        assert node in w.G.nodes
    
    edges = [("john", "likes"), ("john", "dog"), ("likes", "dog"), ("likes", "a"), ("dog", "a"), ("dog", "lot"), ("a", "lot"), ("lot", "likes"), ("dog", "to"), ("likes", "to"), ("likes", "sleep"), ("to", "sleep")]
    for edge in edges:
        assert w.G.has_edge(*edge)

def test_wordweb_construction_punctuation(test_book):
    w = Wordweb(book=test_book, num_of_links_from_new_word=1, punctuation=True)
    print(w.G.nodes)
    assert w.G.number_of_nodes() == 8
    assert w.G.number_of_edges() == 9

    nodes = ["john", "likes", "dog", "a", "lot", ".", "to", "sleep"]
    for node in nodes:
        assert node in w.G.nodes
    
    edges = [("john", "likes"), ("likes", "dog"), ("dog", "a"), ("a", "lot"), ("lot", "."), (".", "dog"), ("dog", "likes"), ("to", "sleep")]
    for edge in edges:
        assert w.G.has_edge(*edge)

def test_wordweb_characteristics(test_book):
    w = Wordweb(book=test_book, num_of_links_from_new_word=1)
    
    assert w.num_of_nodes() == 7
    assert w.avg_k() == pytest.approx(2.0, abs=0.01)
    avg_l, diameter = w.avg_l_and_diameter()
    assert avg_l == pytest.approx(2.14, abs=0.01)
    assert diameter == 4
    assert w.avg_c() == pytest.approx(0.33, abs=0.01)
    assert w.sw_index(w.avg_k(), avg_l, w.avg_c()) == pytest.approx(1.5, abs=0.1)

def test_nodes_difference(test_book):
    w = Wordweb(book=test_book, num_of_links_from_new_word=1, punctuation=True)
    w2 = Wordweb(book=test_book, num_of_links_from_new_word=1, punctuation=False)
    assert w.nodes_difference(w2) == set(["."])
    assert w2.nodes_difference(w) == set(["."])