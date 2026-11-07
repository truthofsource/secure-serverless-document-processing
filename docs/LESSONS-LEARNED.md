# Troubleshooting lessons from the actual platform

These are historical engineering incidents summarized from maintained internal records. They are not newly reproduced tests, a fresh cloud inventory or instructions to repeat a consumed operation. Names, resource identifiers, private payloads and credentials are excluded.

## A clean event still left the document pending

**What happened.** A harmless upload was saved and Event Grid recorded delivery, but the document remained pending. The clean provider result had not completed the application processing chain.

**What the evidence showed.** First, a legacy host-storage setting caused AuthenticationFailed errors. After the narrow setting repair restored polling, the processor rejected the result because a SQL BIGINT file-size value failed its JavaScript integer check. These were configuration and data-shape failures, not one missing-permission problem.

**What changed and how it was checked.** The source query cast an already bounded 1–10 MiB size column to SQL int and added a regression test. A new harmless fixture reached clean and downloaded with matching bytes; the retained original clean event for a separate failed fixture was also verified and replayed unchanged. Temporary queue access was removed.

**What to carry forward.** Trace upload, scan, event delivery, queue processing and SQL state separately. A general BIGINT-to-int cast is unsafe outside this proven bound; do not upload duplicates or manually mark a document clean to make the pipeline appear complete.

Source record: `docs/runbooks/production-private-document-storage-20260925.md — September 25, 2026; docs/troubleshooting/stage2-scan-delivery-and-recovery.md`. These internal paths identify provenance; they are not public file links.

## Evidence and project boundaries

The local examples and screenshots in this repository remain separate from the dated hosted incidents above. A new documentation summary does not establish another successful deployment, restore, security scan or business transaction. Follow the repository’s existing validation guide for the commands and limits of the runnable reference.

The practical sequence is: identify the failing boundary, preserve safe correlation evidence, reconcile any uncertain result, apply only the relevant repair and verify the resulting state. A completed local command is not interchangeable with a completed cloud operation.
