import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.models import Calculation
from app.api.schemas import CalculationCreate


@pytest.fixture(scope="function")
def test_db():
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


def test_calculation_persist_and_read(test_db):
    cc = CalculationCreate(a=1, b=2, type="add")
    calc = Calculation(a=cc.a, b=cc.b, type=cc.type, result=cc.a + cc.b)
    test_db.add(calc)
    test_db.commit()
    test_db.refresh(calc)
    assert calc.id is not None
