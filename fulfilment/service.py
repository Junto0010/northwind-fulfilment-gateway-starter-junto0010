"""Application orchestration: no FastAPI or SQL imports belong here."""
import asyncio
from collections.abc import Iterable
from .carriers import Carrier
from .resilience import CircuitBreaker


async def quote_packages(
    carrier: Carrier, destination: str, quantities: Iterable[int], limit: int, breaker: CircuitBreaker
) -> list[int]:
    """TODO: quote each quantity concurrently, with at most limit in flight, preserving order."""
    semaphore= asyncio.Semaphore(limit)
    async def quote_one(quantity: int) -> int:
        async with semaphore:
            return await breaker.call(lambda: carrier.quote(destination, quantity))
    return await asyncio.gather(*(quote_one(q) for q in quantities))


def customer_summary(rows: Iterable[dict]) -> list[dict]:
    """TODO: produce [{customer_id, shipment_count, quote_cents}] in first-seen order.

    This must handle 100,000 rows in linear time. Do not repeatedly scan a
    growing list to find an existing customer.
    """
    summary: dict[str, dict] = {}
    for row in rows:
        customer_id = row["customer_id"]
        entry = summary.get(customer_id)
        if entry is None:
            entry = {"customer_id": customer_id, "shipment_count": 0, "quote_cents": 0}
            summary[customer_id] = entry
        entry["shipment_count"] += 1
        entry["quote_cents"] += row["quote_cents"]
    return list(summary.values())