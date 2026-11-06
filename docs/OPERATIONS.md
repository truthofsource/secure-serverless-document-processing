# Operations and troubleshooting

## Start and stop

Run unit tests, then start the loopback dashboard with `python -B -m lab serve`. Stop with Ctrl+C. Each demonstration uses disposable synthetic state; running it twice does not send messages or change a cloud resource.

## Diagnose by failure stage

| Symptom | Check and next action |
| --- | --- |
| Upload succeeded but download is blocked | Check current scan state, exact version/ETag and processor health. A stopped nonproduction processor intentionally leaves files pending. |
| Result in dead letter | Verify container routing, event schema, queue permissions and exact file identity before replay. Never manually mark the file clean. |
| New upload shows an old clean state | Compare version binding and UI request ordering. Clear old proof when replacement bytes are stored. |
| AI request failed | Check configured model capability, secret binding, quota and provider status without logging credentials or source documents. Do not automatically repeat paid requests. |

## Cleanup

Default demos use managed temporary directories and close their own database handles. Do not run blanket recursive cleanup against a shared checkout. Inspect `git status --short --ignored`, stop the local server and remove only artifacts you created. Cloud resource cleanup is a separate reviewed operation and is never triggered by this repository's CI.

## Evidence to keep

Retain source commit, test command/exit status, tool versions and safe error stage. For a real release, also retain exact package/image digest and the restored operating state. Do not retain credentials, bearer tokens or employee data in public artifacts.
