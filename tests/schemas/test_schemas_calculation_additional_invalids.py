import pytest

from pydantic import ValidationError

from app.api.schemas import CalculationCreate


def test_invalid_type_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=2, type="noop")
