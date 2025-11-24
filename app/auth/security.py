"""Password hashing utilities using Passlib.

Provides a small, object-oriented wrapper `PasswordHasher` and convenience
module-level helpers `hash_password` and `verify_password` for ease of use in
the rest of the application.
"""
from __future__ import annotations

from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self, schemes: list[str] | None = None, deprecated: str | None = None):
        if schemes is None:
            schemes = ["pbkdf2_sha256"]
        if deprecated is None:
            self._pwd_context = CryptContext(schemes=schemes)
        else:
            self._pwd_context = CryptContext(schemes=schemes, deprecated=deprecated)

    def hash(self, raw_password: str) -> str:
        return self._pwd_context.hash(raw_password)

    def verify(self, raw_password: str, hashed: str) -> bool:
        return self._pwd_context.verify(raw_password, hashed)


_default_hasher = PasswordHasher()


def hash_password(raw_password: str) -> str:
    return _default_hasher.hash(raw_password)


def verify_password(raw_password: str, hashed: str) -> bool:
    return _default_hasher.verify(raw_password, hashed)
