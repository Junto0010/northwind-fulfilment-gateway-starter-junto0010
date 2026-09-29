import asyncio

import pytest

from fulfilment.resilience import CircuitBreaker
from fulfilment.service import quote_packages


@pytest.mark.asyncio
async def test_quotes_are_bounded_concurrent_and_ordered():
    current = maximum = 0

    class Carrier:
        async def quote(self, destination, quantity):
            nonlocal current, maximum
            current += 1
            maximum = max(maximum, current)
            await asyncio.sleep(0.01)
            current -= 1
            return quantity * 100

    result = await quote_packages(Carrier(), "ZA", [3, 1, 2, 4], 2, CircuitBreaker())
    assert result == [300, 100, 200, 400]
    assert maximum == 2


@pytest.mark.asyncio
async def test_open_circuit_does_not_invoke_the_operation(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("fulfilment.resilience.time.time", lambda: now[0])
    breaker, calls = CircuitBreaker(failure_threshold=1, reset_after=10), 0

    async def unavailable():
        nonlocal calls
        calls += 1
        raise ConnectionError()

    with pytest.raises(ConnectionError):
        await breaker.call(unavailable)
    with pytest.raises(RuntimeError):
        await breaker.call(unavailable)
    assert calls == 1
