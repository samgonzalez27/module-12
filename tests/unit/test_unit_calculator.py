"""Unit tests for the calculator functions."""

from app.core.calculator import add, sub, mul, div


def test_add_basic():
    assert add(1, 2) == 3


def test_sub_basic():
    assert sub(5, 3) == 2


def test_mul_basic():
    assert mul(2, 3) == 6


def test_div_basic_and_zero():
    assert div(10, 2) == 5
    import pytest

    with pytest.raises(ZeroDivisionError):
        div(1, 0)
