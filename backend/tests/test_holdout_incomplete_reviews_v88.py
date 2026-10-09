import json
import tempfile
import unittest
from pathlib import Path

from tests.holdout_pipeline_v88 import evaluate_file


class HoldoutIncompleteReviewsV88Tests(unittest.TestCase):
    def test_pending_holdout_cannot_produce_linguistic_metrics(self):
        row = {
            "id": "external-pending-unique-1", "cefr": "A1",
            "objective": "Independently sourced external language sample",
            "exercise": {"type": "translation", "answer": "Die Katze sitzt vor dem Fenster."},
            "learner_answer": "Die Katze sitzt beim Fenster.",
            "source": "external_teacher_casebook", "split": "holdout",
            "human_review": {"status": "pending"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "holdout.jsonl"
            path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            report = evaluate_file(path)
        self.assertEqual(report["release_gate"], "blocked")
        self.assertIn("holdout_reviews_incomplete", report["failed_gates"])
        self.assertEqual(report["pending_review_total"], 1)
        self.assertNotIn("levels", report)


if __name__ == "__main__":
    unittest.main()
