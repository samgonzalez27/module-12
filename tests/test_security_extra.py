from app.auth.security import PasswordHasher


def test_password_hasher_with_deprecated_option():
    hasher = PasswordHasher(schemes=["pbkdf2_sha256"], deprecated="auto")
    raw = "s3cr3t"
    hashed = hasher.hash(raw)
    assert hasher.verify(raw, hashed) is True
    assert hasher.verify("wrong", hashed) is False
