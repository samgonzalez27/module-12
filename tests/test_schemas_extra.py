from datetime import datetime

from app.api.schemas import UserRead


def test_userread_from_attributes():
    class SimpleObj:
        def __init__(self):
            self.id = 42
            self.username = "alice"
            self.email = "alice@example.com"
            self.created_at = datetime.utcnow()

    obj = SimpleObj()
    # model_config sets from_attributes=True so this should validate from attr access
    u = UserRead.model_validate(obj)
    assert u.id == 42
    assert u.username == "alice"
    assert u.email == "alice@example.com"
