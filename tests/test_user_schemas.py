"""Tests for Pydantic user schemas (TDD).

These tests are written first: they define the desired behavior for
`UserCreate` and `UserRead` before the implementation is added.
"""
from datetime import datetime

from app.schemas import UserCreate, UserRead


def test_usercreate_accepts_valid_data():
    uc = UserCreate(username="alice", email="alice@example.com", password="s3cret")
    assert uc.username == "alice"
    assert uc.email == "alice@example.com"
    assert hasattr(uc, "password") and uc.password == "s3cret"


def test_userread_excludes_password_hash_and_maps_from_orm():
    # create a lightweight ORM-like object
    class DummyUser:
        def __init__(self):
            self.id = 1
            self.username = "bob"
            self.email = "bob@example.com"
            self.password_hash = "hashed"
            self.created_at = datetime.utcnow()

    dummy = DummyUser()
    ur = UserRead.model_validate(dummy)

    as_dict = ur.model_dump()
    assert "password_hash" not in as_dict
    assert as_dict["id"] == 1
    assert as_dict["username"] == "bob"
    assert as_dict["email"] == "bob@example.com"
    assert as_dict["created_at"] is not None
