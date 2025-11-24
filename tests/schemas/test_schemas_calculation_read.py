from app.api.schemas import CalculationRead


def test_calculation_read_from_orm_mapping():
    class Dummy:
        def __init__(self):
            self.id = 1
            self.a = 2.0
            self.b = 1.0
            self.type = "add"
            self.result = 3.0

    d = Dummy()
    cr = CalculationRead.model_validate(d)
    assert cr.id == 1
    assert cr.result == 3.0
