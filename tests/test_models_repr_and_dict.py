"""Tests to exercise model `__repr__` and `to_dict` helpers for coverage."""

from app.models import User, Calculation


def test_user_repr_and_to_dict_contains_expected_fields():
    u = User()
    u.id = 10
    u.username = "tester"
    u.email = "t@example.com"
    u.created_at = None

    r = repr(u)
    assert "User" in r and "tester" in r

    d = u.to_dict()
    assert d["id"] == 10
    assert d["username"] == "tester"
    assert d["email"] == "t@example.com"


def test_calculation_repr_and_to_dict_contains_expected_fields():
    c = Calculation()
    c.id = 5
    c.a = 1.25
    c.b = 0.25
    c.type = "add"
    c.result = 1.5

    r = repr(c)
    assert "Calculation" in r and "add" in r

    d = c.to_dict()
    assert d["id"] == 5
    assert d["a"] == 1.25
    assert d["b"] == 0.25
    assert d["type"] == "add"
    assert d["result"] == 1.5
