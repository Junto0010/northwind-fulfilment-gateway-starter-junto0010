"""SQLite persistence boundary. Keep SQL in this module, never in routes."""
import sqlite3
from .domain import Shipment, ShipmentLine


class ShipmentRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS shipments "
            "(id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, destination TEXT NOT NULL, "
            "carrier TEXT NOT NULL, quote_cents INTEGER NOT NULL)"
        )
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS shipment_lines "
            "(shipment_id TEXT NOT NULL, sku TEXT NOT NULL, quantity INTEGER NOT NULL)"
        )

    def save(self, shipment: Shipment) -> None:
        """TODO: persist a shipment and its lines atomically using placeholders."""
        raise NotImplementedError

    def get_for_customer(self, shipment_id: str, customer_id: str) -> Shipment | None:
        """TODO: return only a shipment owned by customer_id; use parameterised SQL."""
        raise NotImplementedError
