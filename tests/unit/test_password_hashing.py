from app.auth.security import PasswordHasher, hash_password, verify_password


def test_password_hash_and_verify():
    hasher = PasswordHasher()
    raw = "secret"
    h = hasher.hash(raw)
    assert hasher.verify(raw, h)
    # module-level helpers
    mh = hash_password("abc123")
    assert verify_password("abc123", mh)
