"""Unit tests for Pydantic schema validation (TDD).

These tests are written first to define expected behavior for schema validation.
"""
import pytest
from pydantic import ValidationError

from app.schemas import UserCreate


def test_usercreate_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="not-an-email", password="pwd")


def test_usercreate_accepts_valid_email():
    u = UserCreate(username="alice", email="alice@example.com", password="pwd")
    assert u.email == "alice@example.com"
