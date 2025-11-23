"""Integration tests for User model against a real Postgres database.

These are intended to run in CI where a Postgres service is provided. Locally
they will be skipped unless `DATABASE_URL` environment variable is set.

The test verifies uniqueness constraints and basic insert/query behavior.
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import User


@pytest.fixture(scope="function")
def pg_session():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        pytest.skip("Skipping Postgres integration tests: DATABASE_URL not set")

    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_postgres_unique_constraints(pg_session):
    u1 = User(username="intuser", email="int@example.com", password_hash="h1")
    u2 = User(username="intuser", email="int2@example.com", password_hash="h2")

    pg_session.add(u1)
    pg_session.commit()

    pg_session.add(u2)
    with pytest.raises(IntegrityError):
        pg_session.commit()


def test_postgres_email_unique(pg_session):
    u1 = User(username="u1", email="unique@example.com", password_hash="h1")
    u2 = User(username="u2", email="unique@example.com", password_hash="h2")

    pg_session.add(u1)
    pg_session.commit()

    pg_session.add(u2)
    with pytest.raises(IntegrityError):
        pg_session.commit()
