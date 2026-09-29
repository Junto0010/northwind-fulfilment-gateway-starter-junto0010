import sqlite3

from fulfilment.domain import Shipment, ShipmentLine
from fulfilment.repository import ShipmentRepository


def test_repository_returns_only_the_owning_customer_shipment():
    repo = ShipmentRepository(sqlite3.connect(":memory:"))
    shipment = Shipment("s-1", "cust-1", "ZA", (ShipmentLine("SKU-1", 2),), "flat-rate", 750)
    repo.save(shipment)
    found = repo.get_for_customer("s-1", "cust-1")
    assert found == shipment
    assert repo.get_for_customer("s-1", "cust-2") is None


def test_repository_treats_injection_text_as_data():
    repo = ShipmentRepository(sqlite3.connect(":memory:"))
    repo.save(Shipment("s-1", "cust-1", "ZA", (), "flat-rate", 500))
    assert repo.get_for_customer("s-1", "cust-1' OR '1'='1") is None
