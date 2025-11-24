import pytest

from fastapi.testclient import TestClient

from app.api import main


client = TestClient(main.app)


def test_division_by_zero_api():
    r = client.get("/div", params={"a": 1, "b": 0})
    assert r.status_code == 400
    assert "division by zero" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_startup_event_runs_and_logs():
    # Directly call the startup event to exercise the simple logging path
    await main.startup_event()