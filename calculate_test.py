import pytest

def calculate_dicount(price: float, discount: float) -> float:
    if not (0 <= discount <= 100):
        raise ValueError("Discount must be between 0 and 100.")
    return price * (1 - discount)

def test_calculate_discount():
    assert calculate_dicount(100, 0.2) == 80.0
    assert calculate_dicount(50, 0) == 50.0
    assert calculate_dicount(200, 1) == 0.0
    with pytest.raises(ValueError):
        assert calculate_dicount(100, -0.1)