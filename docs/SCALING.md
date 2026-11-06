# Scaling, strengths and tradeoffs

## When the workload grows

Use bounded worker concurrency, poison-message isolation and dead-letter monitoring. Store file versions and event journals durably, with per-file atomic state transitions. Limit signed URLs, response sizes and paid AI concurrency. Track oldest pending file, result lag, replay conflicts and queue age. Apply retention to unused derived artifacts without deleting source records or active-issued documents. Require separate commissioning for every new source container.

## Design choices

| Choice | Strength, weakness and tradeoff |
| --- | --- |
| Asynchronous malware checks | Keeps upload requests responsive. Users need clear pending/error feedback and recovery procedures for missed events. |
| Separate processor | Limits business API permissions and isolates event handling. Adds a worker, queue and operational backlog. |
| Version-bound proof | Prevents stale verdicts from authorizing new bytes. Requires exact storage metadata and careful replacement handling. |
| Optional generative AI | Can reduce repetitive preparation work. Adds cost, provider failure modes and output-quality review; it cannot recover truly obscured details reliably. |

## Operating measures

Measure throughput, oldest pending work, duplicate/rejected operations, failure stage and recovery duration. Tie alerts to an operator action. Do not infer service availability from an old successful import or infer delivery from provider acceptance.

Start with measured load and an explicit service objective. Increase concurrency only after checking provider quotas, database contention, per-person ordering and recovery behavior. Horizontal scaling requires a shared durable store; independent in-memory or SQLite processes are not a distributed coordination system.
