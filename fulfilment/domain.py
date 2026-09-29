from dataclasses import dataclass


@dataclass(frozen=True)
class ShipmentLine:
    sku: str
    quantity: int


@dataclass(frozen=True)
class Shipment:
    id: str
    customer_id: str
    destination: str
    lines: tuple[ShipmentLine, ...]
    carrier: str
    quote_cents: int
