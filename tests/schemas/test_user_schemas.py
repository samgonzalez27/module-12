from app.api.schemas import UserCreate, UserRead


def test_user_create_and_read_models():
    uc = UserCreate(username="u", email="u@example.com", password="pw")
    assert uc.username == "u"
    ur = UserRead(id=1, username="u", email="u@example.com")
    d = ur.model_dump()
    assert d["username"] == "u"
