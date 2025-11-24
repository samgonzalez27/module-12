import pytest

from app.core.database import Base
from app.core.models import Calculation, User


def test_compute_result_persists_and_returns():
    # Use an in-memory DB via SQLAlchemy engine in tests that create sessions
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        u = User(username="u", email="u@example.com", password_hash="h")
        db.add(u)
        db.commit()
        db.refresh(u)

        calc = Calculation(a=3.0, b=2.0, type="add", user_id=u.id)
        db.add(calc)
        db.commit()
        db.refresh(calc)

        res = calc.compute_result(persist=True)
        assert res == 5.0
        assert calc.result == 5.0
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
