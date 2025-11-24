from app.core.models import User, Calculation


def test_repr_and_to_dict():
    u = User()
    u.id = 1
    u.username = "me"
    assert "User" in repr(u)
    c = Calculation()
    c.id = 2
    c.a = 1.0
    c.b = 2.0
    c.type = "add"
    d = c.to_dict()
    assert d["id"] == 2
