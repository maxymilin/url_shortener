from http import client
import pytest
from starlette.testclient import TestClient

from shortener_app.main import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client
