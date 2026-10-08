import csv
import tempfile
import unittest
from pathlib import Path

from tests.generate_evaluation_benchmark import build_cases
from tests.linguistic_challenge_suite import build_challenges
from tests.review_evaluation_benchmark import export_packet, import_reviews
from tests.run_evaluation_benchmark import run


class ReviewWorkflowTests(unittest.TestCase):
    def test_export_is_blind_and_import_cannot_approve_itself(self):
        with tempfile.TemporaryDirectory() as directory:
            packet = Path(directory) / "packet.csv"
            reviewed = Path(directory) / "reviewed.jsonl"
            export_packet(packet)
            with packet.open(encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                self.assertNotIn("provisional_expected", reader.fieldnames)
                self.assertNotIn("prediction", reader.fieldnames)
                records = list(reader)
            self.assertEqual(len(records), 480)
            records[0]["decision"] = "correct"
            records[0]["reviewer"] = "external_reviewer"
            with packet.open("w", encoding="utf-8-sig", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
            import_reviews(packet, reviewed)
            import json
            rows = [json.loads(line) for line in reviewed.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(rows[0]["human_review"]["status"], "pending_independence_verification")
            self.assertEqual(run(rows)["reviewed"], 0)

    def test_challenge_packet_is_blind_and_contains_all_levels(self):
        with tempfile.TemporaryDirectory() as directory:
            packet = Path(directory) / "challenge.csv"
            export_packet(packet, build_challenges())
            with packet.open(encoding="utf-8-sig", newline="") as source:
                reader = csv.DictReader(source)
                self.assertNotIn("provisional_expected", reader.fieldnames)
                self.assertNotIn("prediction", reader.fieldnames)
                records = list(reader)
            self.assertEqual(len(records), 40)
            self.assertEqual({r["cefr"] for r in records}, {"A1", "A2", "B1", "B2"})
            self.assertTrue(all(not r["decision"] and not r["reviewer"] for r in records))

    def test_rejects_unsupported_review_decisions(self):
        cases = build_cases()[:1]
        for decision, errors, notes in (
            ("incorrect", "", ""),
            ("correct", "article", ""),
            ("uncertain", "", ""),
        ):
            with self.subTest(decision=decision):
                with tempfile.TemporaryDirectory() as directory:
                    packet = Path(directory) / "packet.csv"
                    export_packet(packet, cases)
                    with packet.open(encoding="utf-8-sig", newline="") as source:
                        records = list(csv.DictReader(source))
                    records[0].update(decision=decision, error_types=errors,
                                      notes=notes, reviewer="external_reviewer")
                    with packet.open("w", encoding="utf-8-sig", newline="") as target:
                        writer = csv.DictWriter(target, fieldnames=records[0].keys())
                        writer.writeheader()
                        writer.writerows(records)
                    with self.assertRaises(ValueError):
                        import_reviews(packet, Path(directory) / "out.jsonl", cases)

    def test_rejects_modified_model_answer(self):
        with tempfile.TemporaryDirectory() as directory:
            packet = Path(directory) / "packet.csv"
            export_packet(packet, build_cases()[:1])
            content = packet.read_text(encoding="utf-8-sig")
            packet.write_text(content.replace("Ich trinke Wasser.", "Ich trinke Saft."), encoding="utf-8")
            with self.assertRaises(ValueError):
                import_reviews(packet, Path(directory) / "output.jsonl", build_cases()[:1])


if __name__ == "__main__":
    unittest.main()
