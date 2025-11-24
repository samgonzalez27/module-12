"""Password hashing utilities using Passlib.

Provides a small, object-oriented wrapper `PasswordHasher` and convenience
module-level helpers `hash_password` and `verify_password` for ease of use in
the rest of the application.
"""
from __future__ import annotations

from passlib.context import CryptContext
import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Any


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


# Minimal JWT-like functions (HMAC-SHA256, no external dependency)
_JWT_SECRET = "dev-secret-change-me"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    padding = 4 - (len(s) % 4)
    if padding != 4:
        s = s + ("=" * padding)
    return base64.urlsafe_b64decode(s.encode("ascii"))


def create_token(payload: Dict[str, Any], secret: str | None = None, expire_seconds: int = 3600) -> str:
    if secret is None:
        secret = _JWT_SECRET
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    body = {**payload, "iat": now, "exp": now + expire_seconds}
    h = json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    p = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    seg1 = _b64url_encode(h)
    seg2 = _b64url_encode(p)
    signing_input = f"{seg1}.{seg2}".encode("ascii")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    seg3 = _b64url_encode(sig)
    return f"{seg1}.{seg2}.{seg3}"


def verify_token(token: str, secret: str | None = None) -> Dict[str, Any] | None:
    if secret is None:
        secret = _JWT_SECRET
    try:
        seg1, seg2, seg3 = token.split(".")
        signing_input = f"{seg1}.{seg2}".encode("ascii")
        sig = _b64url_decode(seg3)
        expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload_bytes = _b64url_decode(seg2)
        payload = json.loads(payload_bytes.decode("utf-8"))
        if "exp" in payload and int(time.time()) > int(payload["exp"]):
            return None
        return payload
    except Exception:
        return None
