from app.core.models import Calculation


def test_calculation_compute_no_persist_and_force():
    c = Calculation()
    c.a = 6
    c.b = 7
    c.type = "multiply"
    c.result = None

    # When persist is False, the in-memory result should remain None
    computed = c.compute_result(persist=False)
    assert computed == 42
    assert c.result is None

    # When force=True, the result should be stored even if previously None
    computed2 = c.compute_result(persist=True, force=True)
    assert computed2 == 42
    assert c.result == 42

    # repr and to_dict should be callable for coverage
    r = repr(c)
    assert "Calculation" in r
    d = c.to_dict()
    assert d["a"] == 6
