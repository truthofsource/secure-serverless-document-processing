# Secure Serverless Document Processing

**An upload is not a clean file, and an AI result is not an access decision.**

![Overview of the working local demonstration](docs/images/01-overview.png)

## Business scenario

Staff and applicants needed to upload sensitive documents, see when file checks completed and retrieve only authorized clean versions. Event delivery could be delayed or duplicated, and optional AI processing needed an explicit trust boundary.

**Business goal:** Automate document handling while preventing stale scan results, duplicate events or optional AI output from bypassing access protection.

## Engineering context

This project distills work I designed and implemented for an Azure-based workforce and operations platform. The organization, people, cloud resource names and records have been anonymized. The public code extracts selected decisions into a runnable reference; it is not a copy of the private production system.

- Centralized document handling through Azure Functions, private storage and authorized staff/applicant access paths, including legacy-source ingestion patterns using Logic Apps.
- Built a dedicated scan-result processor, separate from ordinary business requests, with event/container routing, clean-file proofs and protected downloads.
- Added visible file-check states across upload areas so upload acceptance and clean-file availability were distinct outcomes.
- Implemented employee badge portrait preparation with optional AI assistance, fixed-template rendering and protected employee views; kept original identity documents separate from derived artifacts.

The screenshots are captured from this repository's working **local demonstration with fictional data**. They are not cloud-portal screenshots or claims that a visitor has provisioned these resources. [Evidence and scope](docs/VALIDATION.md) distinguishes implemented platform patterns, local tests and cloud work not commissioned here.

## Architecture

```mermaid
flowchart LR
  User[Staff or applicant] --> API[Authorized upload API]
  API --> Blob[(Private immutable file)]
  Blob --> Scan[Defender malware scan]
  Scan --> Event[Event Grid result]
  Event --> Queue[(Result queue / dead letter)]
  Queue --> Processor[Separate scan processor]
  Processor --> Proof[(Version-bound clean proof)]
  Proof --> Download[Protected file view]
  Download -. optional approved input .-> AI[AI assistance]
```

## Terraform infrastructure

Private intake/deployment containers, result and poison queues, a managed-identity Event Grid topic, optional Defender scan configuration and an optional disabled Functions Flex shell.

See the [Terraform code and validation steps](infra/README.md), [input example](infra/example.tfvars.example) and [mock plan tests](infra/tests). Cloud commissioning and any paid resources remain separate from the local demonstration.

## Run it

Requires Python 3.12 or newer. The identity example also installs its pinned cryptography dependency. Run inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -B -m unittest discover -s tests -v
python -B -m lab demo
python -B -m lab serve --port 8011
```

On Windows, use `.venv\Scripts\Activate.ps1` instead of the `source` command, or run `.venv\Scripts\python.exe` directly. Open [the local workbench](http://127.0.0.1:8011), choose **Run demonstration**, then review **Validation** and **Evidence**. Stop with Ctrl+C. No cloud login, employee data or paid API request is required.

## Validation and failure handling

![Positive and negative checks from the local execution](docs/images/02-validation.png)

Expected security denials count as successful negative tests. The implementation walkthrough explains what each check demonstrates and where the hosted-system boundary begins.

| Read next | Purpose |
| --- | --- |
| [Implementation walkthrough](docs/WALKTHROUGH.md) | Follow the code, business decision and failure case |
| [Architecture](docs/ARCHITECTURE.md) | Understand trust boundaries and cloud integration |
| [Validation evidence](docs/VALIDATION.md) | See actual local results and untested boundaries |
| [Security and privacy](SECURITY.md) | Review permissions, secrets and publication controls |
| [Operations and troubleshooting](docs/OPERATIONS.md) | Diagnose failures and clean up safely |
| [Scaling and tradeoffs](docs/SCALING.md) | Decide when to change the design |
| [Sources and presentation credits](docs/REFERENCES.md) | Technical references and README inspiration |

## Repository map

```text
infra/               Terraform source, example inputs and mock plan tests
lab/                 Working reference implementation and loopback dashboard
tests/               Positive, negative and recovery cases
docs/                Architecture, walkthrough, evidence and operating guide
.github/workflows/   Manual-only contract validation; no cloud deployment
```

## Cost and cleanup

The default local demo creates only temporary local state and makes no paid calls. Cloud examples are separate opt-in source and can create billable resources if an operator applies them. No automated deployment or destruction is configured. Use `git status --short --ignored` before cleanup; remove only your own `.venv` or disposable lab output. Never copy real state files, tokens or employee documents into this repository.
