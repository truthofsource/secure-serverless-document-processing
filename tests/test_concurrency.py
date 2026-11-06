import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from lab.domain import Intake


class ConcurrencyTests(unittest.TestCase):
    def test_duplicate_events_across_worker_connections(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "events.db")
            setup = Intake(path)
            setup.upload("file-001", "employee-001", "version-001", b"synthetic")
            setup.db.close()

            def worker(_):
                adapter = Intake(path)
                try:
                    return adapter.scan(
                        "same-event", "file-001", "version-001", "No threats found"
                    )
                finally:
                    adapter.db.close()

            with ThreadPoolExecutor(max_workers=4) as workers:
                results = list(workers.map(worker, range(4)))
            self.assertEqual(results, ["clean"] * 4)
            check = Intake(path)
            try:
                self.assertEqual(
                    check.db.execute("select count(*) from events").fetchone()[0], 1
                )
            finally:
                check.db.close()

    def test_existing_owner_cannot_be_changed_on_replacement(self):
        adapter = Intake()
        try:
            adapter.upload("file-001", "employee-001", "v1", b"synthetic")
            with self.assertRaises(ValueError):
                adapter.upload("file-001", "employee-002", "v2", b"changed")
        finally:
            adapter.db.close()
