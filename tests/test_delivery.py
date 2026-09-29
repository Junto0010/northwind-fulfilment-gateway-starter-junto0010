from fastapi.testclient import TestClient

from fulfilment.api import build_app


def test_hashed_asset_has_immutable_cache_header():
    response = TestClient(build_app()).get("/assets/app.a1b2c3.js")
    assert response.status_code == 200
    assert "max-age=31536000" in response.headers["cache-control"]
    assert "immutable" in response.headers["cache-control"]
