import pytest
from scripts import utils
import networkx as nx

def test_strip_word():
    assert utils.strip_word("NoInterpunction") == ("nointerpunction", False)

def test_strip_word_interpunction():
    assert utils.strip_word("Interpunction!") == ("interpunction", True)

def test_strip_word_interpunction_in_the_middle():
    assert utils.strip_word("...Don't!!") == ("don't", True)

def test_strip_word_empty():
    assert utils.strip_word("") == ("", False)

def test_strip_word_only_interpunction():
    assert utils.strip_word("???") == ("", True)

def test_split_word():
    assert utils.split_word("NoInterpunction") == ["nointerpunction"]

def test_split_word_interpunction():
    assert utils.split_word("Interpunction!") == ["interpunction", "!"]

def test_split_word_interpunction_multiple():
    assert utils.split_word('"Don\'t!"') == ['"', "don't", "!", '"']

def test_split_word_empty():
    assert utils.split_word("") == []

def test_split_word_only_interpunction():
    assert utils.split_word("???") == ["?", "?", "?"]

def test_multiregime_gammas():
    G = nx.barabasi_albert_graph(50000, 2, seed="thegodseed".__hash__())

    degrees = [k for _, k in G.degree()]
    k, p_k = utils.samples_to_probability(degrees)
    bk, bp_k = utils.log_bin(k, p_k, 35)
    left, right, slope, intercept, r2, confidence = utils.linear_regression(bk, bp_k)
    
    bk = list(bk[left:right])
    bp_k = list(bp_k[left:right])

    assert left <= 5 # not cutting too much

    mid = len(bk) // 2
    bk_small = bk[:mid]
    bp_k_small = bp_k[:mid]
    _, _, slope_small, intercept_small, r2_small, confidence_small = utils.linear_regression(bk_small, bp_k_small, trim_statistics=False)

    bk_large = bk[mid:]
    bp_k_large = bp_k[mid:]
    _, _, slope_large, intercept_large, r2_large, confidence_large = utils.linear_regression(bk_large, bp_k_large, trim_statistics=False)
    
    gamma_1, gamma_2 = -slope_small, -slope_large

    # both regimes should have gamma ~~ 3
    assert gamma_1 < 3.2
    assert gamma_1 > 2.5

    assert gamma_2 < 3.2
    assert gamma_2 > 2.5

def test_from_middle_even():
    array = [0,1,2,3,4]
    left, right, n = utils.from_middle(len(array), 0)
    expected = [2]
    assert n == 1
    assert array[left:right] == expected

    left, right, n = utils.from_middle(len(array), 1)
    expected = [1,2,3]
    assert n == 3
    assert array[left:right] == expected

    left, right, n = utils.from_middle(len(array), 2)
    expected = [0,1,2,3,4]
    assert n == 5
    assert array[left:right] == expected
    
    try:
        left, right, n = utils.from_middle(len(array), 3)
        assert False
    except ValueError:
        pass

def test_from_middle_odd():
    array = [0,1,2,3,4,5]
    left, right, n = utils.from_middle(len(array), 0)
    expected = [2,3]
    assert n == 2
    assert array[left:right] == expected

    left, right, n = utils.from_middle(len(array), 1)
    expected = [1,2,3,4]
    assert n == 4
    assert array[left:right] == expected

    left, right, n = utils.from_middle(len(array), 2)
    expected = [0,1,2,3,4,5]
    assert n == 6
    assert array[left:right] == expected
    
    try:
        left, right, n = utils.from_middle(len(array), 3)
        assert False
    except ValueError:
        pass
