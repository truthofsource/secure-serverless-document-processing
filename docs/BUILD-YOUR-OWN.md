# Build your own from scratch: Secure Serverless Document Processing

Your own private upload quarantine, Defender scan-result delivery and exact-object release decision.

Start with a new folder, your own files and your own accounts. The numbered steps below describe the build; no portfolio repository checkout is required. The existing implementation/evidence elsewhere in this repository is a separate reference, not a claim that your new build has already passed.

## Prerequisites

Azure Storage/Defender for Storage/Event Grid permissions, a chosen scan-volume budget, a private event destination and a serverless consumer identity. Scanning is billed and configuration limits must be checked for the selected account/region.

Use Bash on Linux/macOS/WSL for Bash blocks and PowerShell for PowerShell blocks. Select the tool versions supported by the official sources below, record the versions you actually install and retain generated dependency locks. Cloud resources, scanner downloads, logs and external AI calls can create costs; review the stated scope before enabling them.

## Create your project folder

Choose a new folder name. These first commands create a blank project; an optional `git init` gives it its own history. Create parent directories in your editor when a later step introduces a nested file.

```bash
mkdir my-secure-serverless-document-processing
cd my-secure-serverless-document-processing
git init
```

Create `.gitignore` before saving credentials or build outputs:

```gitignore
.venv/
node_modules/
.env
.env.*
local.settings.json
credentials.json
token.json
*.pem
*.key
*.tfstate*
*.tfplan
.terraform/
private*/
captures/
backups/
batch.json
reports/
out/
app-config.local.yaml
```

The source/file snippets are a starting implementation you type or paste into the named files. Replace `YOUR_*`, names, regions and addresses only with values from your own lab; do not place real client/employee records in a test project. Keep your terminal in this project root unless a step explicitly changes directory.

Before a first commit, set your own repository-local author with `git config user.name "YOUR_NAME"` and `git config user.email "YOUR_PUBLIC_COMMIT_EMAIL"`. Review `git status --short` and the staged diff before publishing; ignored local files are not a substitute for reviewing what you upload.

## Step 1 — Create the upload boundary

**Where:** Azure Portal → Storage account → Containers.

Create a private quarantine container and keep incoming files unavailable to ordinary download users. Define object owner, size/type limits, upload ID and version/ETag fields before connecting a scanner. Record whether the upload is still active; a scan result must never reactivate a retired/revoked upload.

**Check before continuing:** A new upload is Pending and has an exact object identity.

## Step 2 — Enable malware scanning deliberately

**Where:** Storage account → Microsoft Defender for Cloud / Defender for Storage settings.

Enable the supported on-upload malware-scanning feature and set its monthly volume/cost cap. Review account/region support and how unavailable, excluded or oversized files are reported instead of assuming every file will be scanned.

**Check before continuing:** The saved scanning configuration and cap are visible.

## Step 3 — Create the result delivery path

**Where:** Defender scanning Event Grid configuration and your queue/consumer.

Create the supported custom topic/result subscription and a private queue or function endpoint. Configure the actual sender/consumer identities and dead-letter behavior; verify that the scanner can publish and the worker can read only its destination. Select the Event Grid event schema for the example consumer below; a CloudEvents envelope uses different top-level fields and needs a corresponding adapter.

**Check before continuing:** A harmless test upload yields an actual scan-result event at the intended destination.

## Step 4 — Implement the release predicate

**Where:** Your consumer module.

Create release_rule.py below and call it only after authenticating delivery and loading the current stored upload record. It rejects malformed event shapes and inactive records before comparing the exact object/version; it does not itself authenticate delivery or move a blob.

Create **`release_rule.py`** with the following contents:

```python
def can_release(current, event):
    if not isinstance(current, dict) or not isinstance(event, dict):
        return False
    data = event.get('data')
    if not isinstance(data, dict) or current.get('active') is not True:
        return False
    for field in ('blob_uri', 'etag'):
        value = current.get(field)
        if not isinstance(value, str) or not value or value.strip() != value:
            return False
    return (event.get('eventType') == 'Microsoft.Security.MalwareScanningResult'
            and data.get('blobUri') == current['blob_uri']
            and data.get('eTag') == current['etag']
            and data.get('scanResultType') == 'No threats found')

if __name__ == '__main__':
    row = {'blob_uri': 'https://example.invalid/q/test.txt', 'etag': 'version-2', 'active': True}
    event = {'eventType': 'Microsoft.Security.MalwareScanningResult', 'data': {
        'blobUri': row['blob_uri'], 'eTag': 'version-1', 'scanResultType': 'No threats found'}}
    assert not can_release(row, event)
    event['data']['eTag'] = 'version-2'
    assert can_release(row, event)
    assert not can_release({**row, 'active': False}, event)
    assert not can_release(row, {'data': None})
    event['data']['scanResultType'] = 'Error'
    assert not can_release(row, event)
```

Keep the stored and delivered ETag in the same explicitly defined representation. A quote/format mismatch must be investigated in the adapter, not treated as permission to ignore version matching. Malformed/rejected messages need a bounded failure/dead-letter path in the actual consumer.

**Check before continuing:** Only a clean result for the same URI/ETag of an active current upload can pass this narrow predicate.

## Step 5 — Prove clean, blocked and stale outcomes

**Where:** Your approved lab consumer and event history.

Run the local predicate test, then use the official harmless/EICAR testing procedure only in your authorized isolated lab. Verify Pending/Error/Not Scanned remain unavailable, an old result cannot unlock a new version, duplicate delivery is idempotent and a current clean result changes only its intended record.

```bash
python3 release_rule.py
```

**Check before continuing:** Your evidence covers actual scanning/delivery and application release separately.

## Step 6 — Verify download authorization and close out

**Where:** Your own application/API and Azure Portal.

Test an authorized owner and a different user against the saved current file, checking ownership and current clean status again at download. Retain private failure/dead-letter evidence, disable only the lab intake and remove resources under the chosen retention policy.

**Check before continuing:** A scanner verdict alone never grants another person access to a document.

## Verification and your own screenshots

| Evidence | What to record | Your result |
| --- | --- | --- |
| New build | Your own files/resource settings and tool versions | Not yet recorded |
| Working path | The actual successful request, configuration or recovery result | Not yet recorded |
| Failure boundary | A meaningful denied, malformed, stale or failed case | Not yet recorded |
| Recovery / cleanup | What you restored or removed and what remains billed | Not yet recorded |

Capture your own architecture/configuration, one working result and one failure/recovery result. Keep tokens, credentials, personal records and private identifiers out of public screenshots. The architecture diagram explains the design; record your own results rather than treating it as execution evidence.

## Troubleshooting order

1. Confirm the named file, working directory and selected tool/interpreter.
2. Check the exact input and resource/account selected for the failing step.
3. Separate identity permission, network/DNS reachability and application validation.
4. Keep the actual error and reconcile an unknown write outcome before repeating it; do not widen access or repeat paid operations blindly.

The numbered steps describe a build procedure. Local syntax checks, an accepted API request, a completed hosted operation and a human verification are different evidence levels; fill in the verification table with what you actually observed.

## Official implementation references

- [learn.microsoft.com — defender-for-storage-configure-malware-scan](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-configure-malware-scan)
- [learn.microsoft.com — defender-for-storage-test](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-storage-test)
