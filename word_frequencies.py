import pytest

def word_frequencies(text: str) -> dict:
    words = text.split()
    frequencies = {}
    for word in words:
        word = word.lower()
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies

def test_word_frequencies():
    assert word_frequencies("Hello world") == {"hello": 1, "world": 1}
    assert word_frequencies("Hello hello") == {"hello": 2}
    assert word_frequencies("") == {}
    assert word_frequencies("One fish two fish red fish blue fish") == {
        "one": 1,
        "fish": 4,
        "two": 1,
        "red": 1,
        "blue": 1
    }