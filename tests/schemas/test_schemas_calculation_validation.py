import pytest

from pydantic import ValidationError

from app.api.schemas import CalculationCreate


def test_case_insensitive_types_work():
    cc = CalculationCreate(a=1, b=1, type="Add")
    assert cc.type == "add"


def test_additional_invalids_raise():
    with pytest.raises(ValidationError):
        CalculationCreate(a="not-a-number", b=1, type="add")
