from app.api.schemas import CalculationCreate


def test_case_insensitive_type_normalizes():
    cc = CalculationCreate(a=1, b=2, type="Add")
    assert cc.type == "add"
