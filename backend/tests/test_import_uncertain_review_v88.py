import csv
import tempfile
import unittest
from pathlib import Path

from tests.export_uncertain_review_v88 import write_packet
from tests.import_uncertain_review_v88 import import_uncertain


class UncertainReviewImportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"id": "case-1", "cefr": "A1", "objective": "Translate greeting",
             "exercise": {"type": "translation", "answer": "Guten Tag"},
             "learner_answer": "Hallo"}
        ]

    def test_import_requires_reviewer_and_remains_unapproved(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "review.csv"
            manifest = Path(tmp) / "manifest.json"
            output = Path(tmp) / "reviewed.jsonl"
            write_packet(csv_path, manifest, self.rows)
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                records = list(csv.DictReader(handle))
            records[0].update(decision="incorrect", error_types="meaning", reviewer="external-1")
            with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
            result = import_uncertain(csv_path, output, manifest, self.rows)
            self.assertEqual(result["imported_review_count"], 1)
            self.assertEqual(result["levels"]["A1"]["approved_independent"], 0)
            self.assertEqual(result["release_gate"], "blocked")
            self.assertIn("pending_independence_verification", output.read_text())

    def test_missing_manifest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "manifest is required"):
            import_uncertain("unused.csv", "unused.jsonl", rows=self.rows)

    def test_changed_case_content_is_rejected_even_with_same_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "review.csv"
            manifest = Path(tmp) / "manifest.json"
            write_packet(csv_path, manifest, self.rows)
            changed = [{**self.rows[0], "exercise": {"type": "translation", "answer": "Guten Morgen"}}]
            with self.assertRaisesRegex(ValueError, "manifest does not match"):
                import_uncertain(csv_path, Path(tmp) / "reviewed.jsonl", manifest, changed)

    def test_tampered_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "review.csv"
            manifest = Path(tmp) / "manifest.json"
            write_packet(csv_path, manifest, self.rows)
            manifest.write_text('{"case_ids": []}')
            with self.assertRaises(ValueError):
                import_uncertain(csv_path, Path(tmp) / "reviewed.jsonl", manifest, self.rows)


if __name__ == "__main__":
    unittest.main()
