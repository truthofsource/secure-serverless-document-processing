# Malware scanner scaling and tradeoffs

| Choice | Strength | Weakness / tradeoff |
| --- | --- | --- |
| Managed Defender scanning | Uses a maintained detection service rather than building an antivirus engine | Paid service limits, supported inputs and scan latency still need monitoring |
| Asynchronous result queue | Decouples uploads, event delivery and processing | Users need pending status and an operational recovery path |
| Separate Functions processor | Limits business-API privilege and isolates event work | Another runtime/identity/queue must be operated |
| Exact-version clean proof | Stops stale verdicts from releasing replacement bytes | Requires durable metadata and atomic per-file state transitions |
| Logical quarantine | Blocks ordinary application distribution without moving files | Storage operators with separate data permission remain a distinct trust boundary |
| Fail closed on unknown/error | Avoids treating absence of evidence as a clean result | Can reduce availability until the failure is resolved |

Scale from measured arrival rate, average scan size, result lag and queue age. Bound processor concurrency and retry budgets. Use a shared durable journal rather than independent SQLite workers, and serialize or conditionally update each immutable file's state. Isolate poison work and deduplicate before side effects.

Test storage, event-delivery and database limits before raising throughput. A configured data-volume cap is not a hard spending cap. Blob versions, retained failed files, operations and diagnostics can continue to cost money even when a processor is paused. Define investigation/retention ownership before automating deletion.
