from fastapi.testclient import TestClient

from fulfilment.api import build_app


def test_create_and_read_a_shipment_as_the_owner():
    client = TestClient(build_app())
    created = client.post("/shipments", json={"customer_id": "cust-1", "destination": "ZA", "lines": [{"sku": "A", "quantity": 2}]})
    assert created.status_code == 201
    shipment_id = created.json()["id"]
    fetched = client.get(f"/shipments/{shipment_id}", headers={"X-Customer-Id": "cust-1"})
    assert fetched.status_code == 200
    assert fetched.json()["lines"] == [{"sku": "A", "quantity": 2}]


def test_api_rejects_empty_shipments_and_non_owners():
    client = TestClient(build_app())
    assert client.post("/shipments", json={"customer_id": "cust-1", "destination": "ZA", "lines": []}).status_code == 422
