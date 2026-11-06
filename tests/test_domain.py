import json, os, unittest
from unittest.mock import patch
from lab.domain import Intake
from lab.ai import classify


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.i = Intake()
        self.i.upload("file-1", "employee-1", "v1", b"one")

    def tearDown(self):
        self.i.db.close()

    def test_pending_denial(self):
        with self.assertRaises(PermissionError):
            self.i.download("file-1", "employee-1", b"one")

    def test_clean(self):
        self.i.scan("e1", "file-1", "v1", "No threats found")
        self.assertEqual(self.i.download("file-1", "employee-1", b"one"), b"one")

    def test_wrong_owner(self):
        self.i.scan("e1", "file-1", "v1", "No threats found")
        with self.assertRaises(PermissionError):
            self.i.download("file-1", "employee-2", b"one")

    def test_changed_bytes(self):
        self.i.scan("e1", "file-1", "v1", "No threats found")
        with self.assertRaises(PermissionError):
            self.i.download("file-1", "employee-1", b"two")

    def test_duplicate(self):
        self.assertEqual(
            self.i.scan("e1", "file-1", "v1", "No threats found"),
            self.i.scan("e1", "file-1", "v1", "No threats found"),
        )

    def test_conflicting_replay(self):
        self.i.scan("e1", "file-1", "v1", "No threats found")
        with self.assertRaises(ValueError):
            self.i.scan("e1", "file-1", "v1", "Malicious")

    def test_stale_event(self):
        self.i.upload("file-1", "employee-1", "v2", b"two")
        self.assertEqual(
            self.i.scan("e1", "file-1", "v1", "No threats found"), "obsolete"
        )
        with self.assertRaises(PermissionError):
            self.i.download("file-1", "employee-1", b"two")

    def test_unknown_result_fails_closed(self):
        self.assertEqual(
            self.i.scan("e1", "file-1", "v1", "new-provider-value"), "error"
        )

    def test_blocked_is_not_overwritten_clean(self):
        self.i.scan("e1", "file-1", "v1", "Malicious")
        self.assertEqual(
            self.i.scan("e2", "file-1", "v1", "No threats found"), "blocked"
        )

    def test_immutable_version(self):
        with self.assertRaises(ValueError):
            self.i.upload("file-1", "employee-1", "v1", b"two")

    def test_ai_disabled(self):
        with self.assertRaises(PermissionError):
            classify("Synthetic invoice")

    def test_mock_ai_schema(self):
        def transport(body):
            self.assertFalse(body["store"])
            self.assertTrue(body["text"]["format"]["strict"])
            return {
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": json.dumps(
                                    {"category": "invoice", "needs_review": True}
                                ),
                            }
                        ],
                    }
                ],
            }

        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "synthetic-not-a-credential",
                "OPENAI_MODEL": "configured-model",
            },
        ):
            self.assertTrue(
                classify("Synthetic invoice", allow_paid=True, transport=transport)[
                    "needs_review"
                ]
            )

    def test_ai_rejects_incomplete(self):
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "synthetic-not-a-credential",
                "OPENAI_MODEL": "configured-model",
            },
        ):
            with self.assertRaises(ValueError):
                classify(
                    "Synthetic invoice",
                    allow_paid=True,
                    transport=lambda _: {"status": "incomplete"},
                )
