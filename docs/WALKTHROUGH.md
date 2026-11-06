# Malware scanner walkthrough

## 1. Upload into a private, pending state

The application authorizes the upload and records its employee/record binding and immutable storage identity. Quarantine in this design means application retrieval is denied while the file is pending. This reference does not move files between containers or automatically delete malicious content.

## 2. Let the detection service produce the verdict

Microsoft Defender for Storage performs malware detection. Its scan event is delivered through Event Grid and a queue. The separate Functions processor records the result. The detection service and result processor are different components; an upload can stay pending when either the scan or later processing is incomplete.

The extracted policy maps `No threats found` to clean, `Malicious` to malicious, and errors/not-scanned/unknown values to error:

```bash
npm run test:source
```

## 3. Bind the result to the exact file

The hosted system must validate authenticated delivery, storage/container boundary and immutable file metadata. The local adapter models the tied to one exact version state and event journal. An old clean result cannot unlock a replacement file.

```bash
python -B -m unittest discover -s tests -p test_domain.py -k stale_event -v
```

## 4. Handle duplicate or failed events

Identical event replays return the stored outcome. Reusing an event ID with different details is rejected. A malicious result cannot be overwritten by a later clean result in the local model. Failed processing requires investigation/recovery, not a manual clean flag.

```bash
python -B -m unittest discover -s tests -p test_concurrency.py -v
python -B -m unittest discover -s tests -p test_domain.py -k blocked -v
```

## 5. Release only an authorized clean version

A clean verdict alone does not grant another employee access. The local download gate checks owner, state and exact content hash. The cloud read path also requires trusted storage/version metadata and service authorization.

```bash
python -B -m lab demo
```

Inspect pending, clean, blocked and error records, then open the [workbench](http://127.0.0.1:8011) after starting `python -B -m lab serve`. The events are fictional: no malware engine, real sample or Azure scanner is run locally.
