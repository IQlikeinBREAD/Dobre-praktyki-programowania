import pytest

def count_vowels(s: str) -> int:
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

def test_count_vowels():
    assert count_vowels("Python") == 1
    assert count_vowels("AEIOUY") == 5
    assert count_vowels("") == 0
    assert count_vowels("bcd") == 0
    assert count_vowels("Próba żółwia") == 3