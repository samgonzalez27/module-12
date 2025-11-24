import pytest
from pydantic import ValidationError

from app.api.schemas import CalculationCreate


def test_division_by_zero_rejected():
    with pytest.raises(ValidationError):
        CalculationCreate(a=1, b=0, type="divide")
