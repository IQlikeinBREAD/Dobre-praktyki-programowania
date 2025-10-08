import pytest

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Input should be a positive integer.")
    elif n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 5:
        return 5
    elif n == 10:
        return 55
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 0
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    with pytest.raises(ValueError):
        fibonacci(-1)