"""Version-bound scan results and protected document access."""

import hashlib
import json
import sqlite3


class Intake:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path, isolation_level=None, timeout=5)
        self.db.executescript(
            """create table if not exists files(id text primary key,owner text not null,version text not null,hash text not null,state text not null);
        create table if not exists events(id text primary key,hash text not null,outcome text not null);"""
        )

    def upload(self, file_id, owner, version, data):
        if (
            not all(isinstance(x, str) and x for x in [file_id, owner, version])
            or not data
        ):
            raise ValueError("Required upload identity is missing")
        # In the live service version is the immutable storage version/ETag.
        self.db.execute("begin immediate")
        try:
            prior = self.db.execute(
                "select version,owner from files where id=?", (file_id,)
            ).fetchone()
            if prior and (prior[0] == version or prior[1] != owner):
                raise ValueError(
                    "An immutable version or existing owner cannot be overwritten"
                )
            self.db.execute(
                "insert into files values(?,?,?,?,?) on conflict(id) do update set version=excluded.version,hash=excluded.hash,state=excluded.state",
                (file_id, owner, version, hashlib.sha256(data).hexdigest(), "pending"),
            )
            self.db.execute("commit")
        except Exception:
            self.db.execute("rollback")
            raise

    def scan(self, event_id, file_id, version, result):
        if not all(
            isinstance(x, str) and x for x in [event_id, file_id, version, result]
        ):
            raise ValueError("Malformed scan event")
        fingerprint = hashlib.sha256(
            json.dumps([file_id, version, result], separators=(",", ":")).encode()
        ).hexdigest()
        self.db.execute("begin immediate")
        try:
            prior = self.db.execute(
                "select hash,outcome from events where id=?", (event_id,)
            ).fetchone()
            if prior:
                if prior[0] != fingerprint:
                    raise ValueError("Conflicting event replay")
                outcome = prior[1]
            else:
                row = self.db.execute(
                    "select version from files where id=?", (file_id,)
                ).fetchone()
                if not row or row[0] != version:
                    outcome = "obsolete"
                else:
                    state = {"No threats found": "clean", "Malicious": "blocked"}.get(
                        result, "error"
                    )
                    # A contradictory result cannot turn an already blocked file clean.
                    self.db.execute(
                        "update files set state=case when state='blocked' then 'blocked' else ? end where id=?",
                        (state, file_id),
                    )
                    outcome = self.db.execute(
                        "select state from files where id=?", (file_id,)
                    ).fetchone()[0]
                self.db.execute(
                    "insert into events values(?,?,?)", (event_id, fingerprint, outcome)
                )
            self.db.execute("commit")
            return outcome
        except Exception:
            self.db.execute("rollback")
            raise

    def download(self, file_id, actor, data):
        row = self.db.execute(
            "select owner,hash,state from files where id=?", (file_id,)
        ).fetchone()
        if not row or row[0] != actor:
            raise PermissionError("No access to this document")
        if row[2] != "clean" or row[1] != hashlib.sha256(data).hexdigest():
            raise PermissionError("Exact file has not passed its check")
        return data


def demo():
    intake = Intake()
    data = b"Synthetic portrait placeholder, not an actual ID"
    intake.upload("upload-001", "employee-001", "version-001", data)
    checks = []

    def denied(name, call):
        try:
            call()
            passed = False
        except PermissionError:
            passed = True
        checks.append(
            {
                "name": name,
                "passed": passed,
                "detail": "Expected protected-download denial observed",
            }
        )

    denied(
        "Pending file cannot be downloaded",
        lambda: intake.download("upload-001", "employee-001", data),
    )
    state = intake.scan("event-001", "upload-001", "version-001", "No threats found")
    checks.append(
        {
            "name": "Exact version becomes available after clean result",
            "passed": state == "clean"
            and intake.download("upload-001", "employee-001", data) == data,
            "detail": "Ownership, state and content hash checked",
        }
    )
    checks.append(
        {
            "name": "Duplicate event is idempotent",
            "passed": intake.scan(
                "event-001", "upload-001", "version-001", "No threats found"
            )
            == "clean",
            "detail": "No duplicate processing",
        }
    )
    denied(
        "Another employee cannot fetch this file",
        lambda: intake.download("upload-001", "employee-002", data),
    )
    intake.upload("upload-001", "employee-001", "version-002", b"New synthetic version")
    checks.append(
        {
            "name": "Old clean result cannot unlock replacement",
            "passed": intake.scan(
                "event-002", "upload-001", "version-001", "No threats found"
            )
            == "obsolete",
            "detail": "Immutable version mismatch leaves current upload pending",
        }
    )
    denied(
        "A changed payload cannot reuse a clean proof",
        lambda: intake.download("upload-001", "employee-001", data),
    )
    malicious = b"Fictional file represented by a malicious verdict"
    intake.upload("upload-002", "employee-001", "version-001", malicious)
    intake.scan("event-003", "upload-002", "version-001", "Malicious")
    denied(
        "Malicious verdict keeps the file unavailable",
        lambda: intake.download("upload-002", "employee-001", malicious),
    )
    unknown = b"Fictional file with an unknown result"
    intake.upload("upload-003", "employee-001", "version-001", unknown)
    intake.scan("event-004", "upload-003", "version-001", "Unknown provider value")
    denied(
        "Unknown scan result fails closed",
        lambda: intake.download("upload-003", "employee-001", unknown),
    )
    intake.db.close()
    return {
        "checks": checks,
        "metrics": [
            {
                "label": "Version-bound checks",
                "value": str(len(checks)),
                "detail": "Positive and negative paths",
            },
            {
                "label": "Unverified downloads",
                "value": "0",
                "detail": "Pending remains blocked",
            },
            {
                "label": "File states",
                "value": "4",
                "detail": "Pending, clean, blocked and error",
            },
            {"label": "Cloud writes", "value": "0", "detail": "Local event adapter"},
        ],
        "records": [
            ["upload-001 / v1", "Clean", "Exact content hash and owner verified"],
            ["event-001", "Duplicate", "Original outcome returned"],
            ["upload-001 / v2", "Pending", "Old scan cannot unlock new bytes"],
            [
                "upload-002 / v1",
                "Blocked",
                "Malicious fixture verdict; retrieval denied",
            ],
            ["upload-003 / v1", "Error", "Unknown fixture verdict; retrieval denied"],
        ],
    }
