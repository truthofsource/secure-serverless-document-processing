# Malware scanning operations and troubleshooting

## Understand the four states

| State | Meaning | Allowed next action |
| --- | --- | --- |
| Pending | No accepted result for the current immutable file | Wait/investigate; keep retrieval blocked |
| Clean | An accepted clean proof matches the current file | Allow only the authorized record owner/staff read |
| Blocked | A malicious result was recorded | Keep unavailable; follow security investigation/retention procedure |
| Error / unavailable | Error, not-scanned, unknown value or unresolved processing | Investigate the failure; do not treat it as clean |

`No threats found` is a scanner result, not a guarantee of harmlessness or a substitute for authorization.

## Diagnose by component

| Symptom | Check | Response |
| --- | --- | --- |
| Upload stored but remains pending | Is Defender scanning enabled, within supported limits and producing results? | Check the service before assuming a worker bug |
| Provider result exists but file remains pending | Event subscription, destination queue, processor state and permissions | A paused processor cannot save the result; restore only through an authorized operating window |
| Queue message fails repeatedly | Event schema, trusted source/container, immutable version and database result | Preserve a safe error stage and isolate/review failed work |
| An old result arrives | Compare exact immutable version/ETag and current record | Record/ignore stale result; do not unlock replacement bytes |
| Clean file cannot be opened | Employee binding, record permission, clean proof and exact bytes | Check authorization separately from malware state |
| Malicious result appears | Provider identity and saved file binding | Keep blocked; do not download casually or overwrite the verdict |

## Recovery

Inventory the exact event and file before replay. Verify the provider/event ID, storage host/container, version/ETag, ownership and current saved state. Confirm the worker dependency and permission issue is fixed. Replay only the reviewed item, check one durable outcome and restore any temporary access/service state. Do not invent a clean verdict or replay a broad queue merely to clear a badge.

## Monitoring

Track oldest pending upload, scan-to-event delay, queue age/depth, poison count, rejected source/version events and saved-result failures. Keep detector health distinct from processor health. A registered event subscription does not establish successful delivery.

## Local commands

```bash
npm run test:source
python -B -m unittest discover -s tests -v
python -B -m lab demo
```

The [command guide](COMMANDS.md) explains setup and expected output. These commands use fictional events and make no cloud changes.
