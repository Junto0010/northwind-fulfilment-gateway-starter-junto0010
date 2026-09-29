"""Application orchestration: no FastAPI or SQL imports belong here."""
import asyncio
from collections.abc import Iterable
from .carriers import Carrier
from .resilience import CircuitBreaker


async def quote_packages(
    carrier: Carrier, destination: str, quantities: Iterable[int], limit: int, breaker: CircuitBreaker
) -> list[int]:
    """TODO: quote each quantity concurrently, with at most limit in flight, preserving order."""
    raise NotImplementedError


def customer_summary(rows: Iterable[dict]) -> list[dict]:
    """TODO: produce [{customer_id, shipment_count, quote_cents}] in first-seen order.

    This must handle 100,000 rows in linear time. Do not repeatedly scan a
    growing list to find an existing customer.
    """
    raise NotImplementedError
