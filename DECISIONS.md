# Engineering Decisions

## 1. Carrier Extension Boundary

The system uses a `Carrier` protocol as the boundary between the fulfilment service and individual carrier implementations. The protocol defines the `quote(destination, quantity)` operation that every carrier must provide. The carrier registry created by `build_carriers()` maps public carrier names to their implementations.

This means the service depends on the `Carrier` interface rather than directly depending on `FlatRateCarrier`. To add a new carrier, I only need to implement the same `Carrier` protocol and register the new carrier in the carrier registry. The main fulfilment orchestration does not need to be rewritten.

## 2. Bounded Concurrency and Downstream Protection

Package shipping quotes are requested asynchronously with a bounded concurrency limit. The limit prevents the application from creating an unlimited number of simultaneous requests to the downstream carrier.

The supplied circuit breaker provides additional protection. When repeated carrier failures occur, the circuit breaker stops sending requests for a period and fails fast instead. This prevents continued pressure on an unavailable downstream service while allowing the application to recover when the carrier becomes available again.

Package results are also kept in their original order so that asynchronous execution does not change the expected response ordering.

## 3. Performance Measurement

I validated the operations summary using:

`python -m pytest -q`

**Input size:** 100,000 shipment rows

**Elapsed time:2.3440545s

The measurement showed that the summary operation remained responsive at the required input size. The implementation uses a single-pass aggregation approach rather than repeatedly scanning the complete shipment collection for each customer, giving the core aggregation linear-time behaviour, O(n), with respect to the number of shipment rows.

1. Explain the boundary that lets a new carrier be added with minimal change.
2. Explain your concurrency limit and what protects the downstream carrier.
3. Record one command, input size, and measurement used to validate performance.
