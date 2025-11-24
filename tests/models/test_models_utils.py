from app.core.models import User


def test_user_to_dict_omits_password():
    u = User()
    u.id = 1
    u.username = "user"
    u.email = "a@b.com"
    u.password_hash = "secret"
    d = u.to_dict()
    assert "password_hash" not in d
    assert d["username"] == "user"
