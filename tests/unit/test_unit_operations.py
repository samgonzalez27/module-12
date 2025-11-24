"""Unit tests for the operations compatibility module."""

from app.core.operations import add, sub, mul, div


def test_operations_forwarding():
    assert add(1, 1) == 2
    assert sub(5, 3) == 2
    assert mul(2, 4) == 8
    assert div(9, 3) == 3
