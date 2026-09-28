import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import session_store


@pytest.fixture(autouse=True)
def _reset_session_store():
    """Sessions live in a process-global in-memory dict, so we clear it
    before every test to keep tests independent of run order."""
    session_store.clear_all()
    yield
    session_store.clear_all()


@pytest.fixture
def client():
    return TestClient(app)
