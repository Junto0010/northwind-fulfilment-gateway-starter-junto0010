import time
from collections.abc import Awaitable, Callable
from typing import TypeVar

from fulfilment.carriers import CarrierUnavailable

T = TypeVar("T")


class CircuitBreaker:
    """TODO: implement closed, open, and cooldown/half-open behaviour."""

    def __init__(self, failure_threshold: int = 3, reset_after: float = 10.0) -> None:
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.reset_after = reset_after
        self.opened_at: float | None = None

    def is_open(self) -> bool:
        if self.opened_at is None:
            return False
        return time.time() - self.opened_at < self.reset_after
         

    async def call(self, operation: Callable[[], Awaitable[T]]) -> T:
        if self.is_open():
            raise CarrierUnavailable("Circuit breaker is open. Operation not allowed.")
        try:
            result = await operation()
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.opened_at = time.time()
            raise
        else:
            self.failures = 0
            self.opened_at = None
            return result