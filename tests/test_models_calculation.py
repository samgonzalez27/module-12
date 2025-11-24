"""Tests for the Calculation SQLAlchemy model."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Calculation


@pytest.fixture(scope="function")
def test_db():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_calculation_creation(test_db):
    calc = Calculation(a=1.5, b=2.5, type="add", result=4.0)
    test_db.add(calc)
    test_db.commit()
    test_db.refresh(calc)

    assert calc.id is not None
    assert isinstance(calc.a, float)
    assert isinstance(calc.b, float)
    assert calc.type == "add"
    assert calc.result == 4.0


def test_result_nullable(test_db):
    calc = Calculation(a=3.0, b=1.0, type="subtract")
    test_db.add(calc)
    test_db.commit()
    test_db.refresh(calc)

    assert calc.result is None


def test_type_required(test_db):
    # Omitting required `type` should raise on commit
    calc = Calculation(a=1.0, b=2.0, type=None)  # type: ignore[arg-type]
    test_db.add(calc)
    with pytest.raises(Exception):
        test_db.commit()
