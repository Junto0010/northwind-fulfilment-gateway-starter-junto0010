import time

from fulfilment.service import customer_summary


def test_customer_summary_is_correct_and_fast_at_course_scale():
    rows = [{"customer_id": f"c-{n % 500}", "quote_cents": 100} for n in range(100_000)]
    started = time.perf_counter()
    result = customer_summary(rows)
    elapsed = time.perf_counter() - started
    assert len(result) == 500
    assert result[0] == {"customer_id": "c-0", "shipment_count": 200, "quote_cents": 20_000}
    assert elapsed < 1.5, f"Expected an O(n) solution, got {elapsed:.2f}s"
