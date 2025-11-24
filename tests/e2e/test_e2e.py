from fastapi.testclient import TestClient
from app.api.main import app


def test_basic_end_to_end():
    client = TestClient(app)
    r = client.get("/add", params={"a": 2, "b": 3})
    assert r.status_code == 200
    assert r.json()["result"] == 5
