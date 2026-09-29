"""HTTP adapter. Complete routes by delegating to the domain/service layers."""
import sqlite3
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from starlette.middleware.gzip import GZipMiddleware

from .carriers import build_carriers
from .domain import Shipment, ShipmentLine
from .repository import ShipmentRepository
from .resilience import CircuitBreaker
from .service import quote_packages


class LineIn(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class ShipmentIn(BaseModel):
    customer_id: str = Field(min_length=1)
    destination: str = Field(min_length=2)
    carrier: str = "flat-rate"
    lines: list[LineIn]


def build_app() -> FastAPI:
    app = FastAPI(title="Northwind Fulfilment Gateway")
    app.add_middleware(GZipMiddleware, minimum_size=500)
    repository = ShipmentRepository(sqlite3.connect(":memory:", check_same_thread=False))
    carriers = build_carriers()
    breaker = CircuitBreaker()

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/assets/app.a1b2c3.js")
    async def asset():
        from fastapi.responses import Response
        return Response("console.log('northwind')", media_type="application/javascript",
                        headers={"Cache-Control": "public, max-age=31536000, immutable"})

    @app.post("/shipments", status_code=201)
    async def create_shipment(request: ShipmentIn):
        if not request.lines:
            raise HTTPException(422, "A shipment needs at least one line.")
        carrier = carriers.get(request.carrier)
        if carrier is None:
            raise HTTPException(422, "Unknown carrier.")
        quotes = await quote_packages(carrier, request.destination, (line.quantity for line in request.lines), 5, breaker)
        shipment = Shipment(str(uuid4()), request.customer_id, request.destination,
                            tuple(ShipmentLine(line.sku, line.quantity) for line in request.lines),
                            request.carrier, sum(quotes))
        repository.save(shipment)
        return {"id": shipment.id, "customer_id": shipment.customer_id, "quote_cents": shipment.quote_cents,
                "line_count": len(shipment.lines)}

    @app.get("/shipments/{shipment_id}")
    async def get_shipment(shipment_id: str, x_customer_id: str = Header()):
        shipment = repository.get_for_customer(shipment_id, x_customer_id)
        if shipment is None:
            raise HTTPException(404, "Shipment not found.")
        return {"id": shipment.id, "customer_id": shipment.customer_id, "destination": shipment.destination,
                "carrier": shipment.carrier, "quote_cents": shipment.quote_cents,
                "lines": [{"sku": line.sku, "quantity": line.quantity} for line in shipment.lines]}

    return app


app = build_app()
