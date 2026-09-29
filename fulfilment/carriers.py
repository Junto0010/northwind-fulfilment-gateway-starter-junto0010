"""Carrier strategy boundary. Add a carrier by implementing Carrier and registering it."""
from typing import Protocol


class Carrier(Protocol):
    async def quote(self, destination: str, quantity: int) -> int: ...


class CarrierUnavailable(RuntimeError):
    pass


class FlatRateCarrier:
    async def quote(self, destination: str, quantity: int) -> int:
        """A deterministic local stand-in for a network carrier."""
        return 500 + quantity * 125


def build_carriers() -> dict[str, Carrier]:
    """TODO: return the configured carrier strategies keyed by public name."""
    return {"flat-rate": FlatRateCarrier()}
