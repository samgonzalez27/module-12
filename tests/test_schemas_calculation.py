"""Tests for Pydantic Calculation schemas (TDD)."""

import pytest

from pydantic import ValidationError

from app.schemas import CalculationCreate, CalculationRead


def test_calculationcreate_accepts_valid_data():
    cc = CalculationCreate(a=1, b=2, type="add")
    assert cc.a == 1
    assert cc.b == 2
    assert cc.type == "add"


def test_invalid_type_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=2, type="noop")


def test_calculationread_maps_from_orm():
    class DummyCalc:
        def __init__(self):
            self.id = 1
            self.a = 2.5
            self.b = 1.5
            self.type = "subtract"
            self.result = 1.0

    dummy = DummyCalc()
    cr = CalculationRead.model_validate(dummy)
    as_dict = cr.model_dump()
    assert as_dict["id"] == 1
    assert as_dict["type"] == "subtract"
    assert as_dict["result"] == 1.0
