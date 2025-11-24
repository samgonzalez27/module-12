from fastapi.testclient import TestClient
from app.api.main import app


client = TestClient(app)


def test_add_endpoint():
    r = client.get("/add", params={"a": 1, "b": 2})
    assert r.status_code == 200
    assert r.json()["result"] == 3
