import csv
import json
import tempfile
import unittest
from pathlib import Path

from tests.export_uncertain_review_v88 import select_uncertain, write_packet


class UncertainReviewPacketTests(unittest.TestCase):
    def test_selects_only_unverified_and_preserves_provenance(self):
        rows = [
            {"id": "a", "cefr": "A1", "objective": "x", "exercise": {"type": "translation", "answer": "Hallo"},
             "learner_answer": "Hallo"},
            {"id": "b", "cefr": "B2", "objective": "x", "exercise": {"type": "translation", "answer": "Hallo"},
             "learner_answer": "Servus"},
        ]
        selected, manifest = select_uncertain(rows)
        self.assertEqual([row["id"] for row in selected], ["b"])
        self.assertEqual(manifest["counts_by_level"]["B2"], 1)
        self.assertFalse(manifest["independent_holdout"])
        self.assertEqual(manifest["release_gate"], "blocked")

    def test_packet_is_blind_and_has_matching_manifest(self):
        rows = [{"id": "b", "cefr": "A2", "objective": "translate",
                 "exercise": {"type": "translation", "answer": "Guten Tag"},
                 "learner_answer": "Hallo"}]
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "review.csv"
            manifest_path = Path(tmp) / "manifest.json"
            write_packet(csv_path, manifest_path, rows)
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                records = list(csv.DictReader(handle))
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["decision"], "")
            self.assertIn("question", records[0])
            self.assertNotIn("evaluation_status", records[0])
            self.assertNotIn("provisional_expected", records[0])
            self.assertEqual(json.loads(manifest_path.read_text())["case_ids"], ["b"])

    def test_duplicate_ids_fail_closed(self):
        row = {"id": "duplicate", "cefr": "A1", "exercise": {"type": "translation", "answer": "x"},
               "learner_answer": "y"}
        with self.assertRaises(ValueError):
            select_uncertain([row, row])


if __name__ == "__main__":
    unittest.main()
