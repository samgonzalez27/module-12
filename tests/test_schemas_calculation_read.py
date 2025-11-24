"""Tests for CalculationRead schema to ensure it includes expected fields."""

from app.schemas import CalculationRead


def test_calculationread_includes_user_id_and_fields():
    class DummyCalc:
        def __init__(self):
            self.id = 42
            self.a = 3.5
            self.b = 2.0
            self.type = "multiply"
            self.result = 7.0
            self.user_id = 99

    dummy = DummyCalc()
    cr = CalculationRead.model_validate(dummy)
    d = cr.model_dump()

    assert d["id"] == 42
    assert d["a"] == 3.5
    assert d["b"] == 2.0
    assert d["type"] == "multiply"
    assert d["result"] == 7.0
    assert d["user_id"] == 99
