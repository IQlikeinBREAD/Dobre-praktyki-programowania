import pytest

def is_pylidrome(text:str) -> bool:
    cleaned = ''.join(c.lower() for c in text if not c.isspace())
    return cleaned == cleaned[::-1]

def test_is_pylidrome():
    assert is_pylidrome("kajak") == True
    assert is_pylidrome("A to kanapa pana Kota") == True
    assert is_pylidrome("Jabko") == False
    assert is_pylidrome(" ") == True
    assert is_pylidrome("") == True
