import pytest

def is_pylidrome(text:str) -> bool:
    cleaned = ''.join(c.lower() for c in text if not c.isspace())
    return cleaned == cleaned[::-1]

print(is_pylidrome("kajak"))
print(is_pylidrome("A to kanapa pana Kota"))
print(is_pylidrome("Jabko"))
print(is_pylidrome(" "))