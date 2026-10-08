import csv
import tempfile
import unittest
from pathlib import Path

from tests.review_evaluation_benchmark import export_packet, import_reviews


class ReviewerQuestionIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{"id": "question-1", "cefr": "A1", "objective": "translate",
                      "exercise": {"type": "translation", "question": "Translate: I live here.",
                                   "answer": "Ich wohne hier."},
                      "learner_answer": "Ich lebe hier."}]

    def test_original_question_is_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = Path(tmp) / "review.csv"
            export_packet(packet, self.rows)
            with packet.open(encoding="utf-8-sig", newline="") as handle:
                record = next(csv.DictReader(handle))
            self.assertEqual(record["question"], "Translate: I live here.")
            self.assertEqual(record["decision"], "")

    def test_modified_question_cannot_be_imported(self):
        with tempfile.TemporaryDirectory() as tmp:
            packet = Path(tmp) / "review.csv"
            export_packet(packet, self.rows)
            with packet.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                fields, records = reader.fieldnames, list(reader)
            records[0]["question"] = "Translate: I live elsewhere."
            records[0]["decision"] = "correct"
            records[0]["reviewer"] = "External reviewer"
            with packet.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(records)
            with self.assertRaisesRegex(ValueError, "content changed"):
                import_reviews(packet, Path(tmp) / "reviewed.jsonl", self.rows)


if __name__ == "__main__":
    unittest.main()
