# Commands and expected results

Run from the repository root. These commands reproduce local source/reference checks; they do not apply Azure resources.

## Setup

Use Python 3.12 and Node 22.18+ (accepted run: Node 22.23.2). Bash / Linux / macOS / WSL:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

PowerShell, without changing execution policy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm.cmd run test:source
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

## Run source tests and local demonstration

```bash
npm run test:source
python -B -m unittest discover -s tests -v
python -B -m lab demo
python -B -m lab serve --port 8011
```

The Node runner prints TAP counts; Python ends in `OK`. The CLI report contains checks with `passed: true`. Open [the workbench](http://127.0.0.1:8011), run the demonstration and inspect Validation/Evidence. Stop with Ctrl+C. If a check fails, preserve its error stage rather than editing the success labels.

## Scanner-specific checks

```bash
node --experimental-strip-types --test reference/scan-result-policy.test.ts
python -B -m unittest discover -s tests -p test_domain.py -k stale_event -v
python -B -m unittest discover -s tests -p test_domain.py -k blocked -v
python -B -m unittest discover -s tests -p test_concurrency.py -v
```

`npm run test:source` runs the extracted provider mapping; Python exercises the public event/version journal. `OK` on a malicious-file test means its download was denied, not that the file was made clean. No live malware sample or Defender scan is performed.


## Terraform without cloud mutation

```bash
terraform -chdir=infra init -backend=false -input=false
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
terraform -chdir=infra test -filter=tests/intake.tftest.hcl
```

Initialization downloads the pinned providers. `validate` checks schema; the tests use mock providers and plan commands. They do not prove live RBAC, DNS or provider behavior. Example inputs contain placeholders, never a real backend or secret value. No apply/destroy is part of the local procedure.

## Manual CI

The workflow sets up Python and Node, runs `npm run test:source`, installs declared Python dependencies, runs the Python tests and executes the local demo. It is manual-only; documenting it does not dispatch a workflow or spend Actions minutes.

## Local inspection

```bash
git status --short --ignored
git diff --check
```

Keep source documents, credentials, state/plans and sensitive reports out of Git. No Azure service start, provider connection, message or paid request is required to reproduce the included screenshots.
