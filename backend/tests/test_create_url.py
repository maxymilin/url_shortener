import json
from multiprocessing.context import assert_spawning

import pytest

from shortener_app.main import app


def test_create_url(test_app, monkeypatch):
    test_request_payload = {"target_url": "https://wwww.google.com"}
    test_response_payload = {"target_url": "https://wwww.google.com", "key": "AAAAA"}

    async def mock_post(payload):
        return 1

    monkeypatch.settart(app, "shorten_url", mock_post)

    response = test_app.post("shorten_url", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload
