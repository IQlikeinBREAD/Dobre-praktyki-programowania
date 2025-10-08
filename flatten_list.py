import pytest

def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list

def test_flatten():
    assert flatten([1, 2, [3, 4], [[5]], 6]) == [1, 2, 3, 4, 5, 6]
    assert flatten([]) == []
    assert flatten([[[[1]]]]) == [1]
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]
    assert flatten([1, 2, 3]) == [1, 2, 3]