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
        with self.connection:
            self.connection.execute(
                "INSERT INTO shipments VALUES (?, ?, ?, ?, ?)",
                (shipment.id, shipment.customer_id, shipment.destination, shipment.carrier, shipment.quote_cents)
            )
            self.connection.executemany(
                "INSERT INTO shipment_lines (shipment_id, sku, quantity) VALUES (?, ?, ?)",
                ((shipment.id, line.sku, line.quantity) for line in shipment.lines),
            )

    def get_for_customer(self, shipment_id: str, customer_id: str) -> Shipment | None:
        """TODO: return only a shipment owned by customer_id; use parameterised SQL."""
        shipment_row = self.connection.execute(
            "SELECT id, customer_id, destination, carrier, quote_cents "
            "FROM shipments WHERE id = ? AND customer_id = ?",
            (shipment_id, customer_id),
        ).fetchone()
        if shipment_row is None:
            return None
        lines = tuple(
            ShipmentLine(sku, quantity)
            for sku, quantity in self.connection.execute(
                "SELECT sku, quantity FROM shipment_lines WHERE shipment_id = ? ORDER BY rowid",
                (shipment_id,),
            )
        )
        return Shipment(
            id=shipment_row[0],
            customer_id=shipment_row[1],
            destination=shipment_row[2],
            lines=lines,
            carrier=shipment_row[3],
            quote_cents=shipment_row[4],
        )
    
