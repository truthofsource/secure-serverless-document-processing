# Implementation source map

This is a case study of the malware-scanning controls built for the actual workforce platform.

| Public file | Relationship to the implementation |
| --- | --- |
| `reference/scan-result-policy.ts` | Extracted provider-result mapping; only the product-specific type name was made neutral |
| `reference/scan-result-policy.test.ts` | Actual mapping tests with a portable TypeScript import |
| `lab/domain.py` | A compact Python reference for the event/version journal and protected retrieval boundary; not the hosted Node.js worker |
| `infra/events.tf` | Related Defender/Event Grid/queue resource patterns with neutral names and explicit Off controls |
| `infra/processor.tf` | Disabled processor shell, not a published application package |

The hosted system additionally validates provider delivery, storage/container allowlists, ETags/version IDs, file metadata and SQL processing. Those cloud adapters are not replaced by a test-only JSON event. The public demo never scans a real file for malware.

Badge portrait generation is a separate project. This repository contains no image-generation or text-classification adapter.
