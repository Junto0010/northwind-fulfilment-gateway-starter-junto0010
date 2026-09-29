import time
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class CircuitBreaker:
    """TODO: implement closed, open, and cooldown/half-open behaviour."""

    def __init__(self, failure_threshold: int = 3, reset_after: float = 10.0) -> None:
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.reset_after = reset_after
        self.opened_at: float | None = None

    def is_open(self) -> bool:
        raise NotImplementedError

    async def call(self, operation: Callable[[], Awaitable[T]]) -> T:
        raise NotImplementedError
