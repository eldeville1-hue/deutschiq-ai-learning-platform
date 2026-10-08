import json
import tempfile
import unittest
from pathlib import Path

from tests.holdout_pipeline_v88 import check_holdout, evaluate_file, load_holdout
from tests.generate_curated_evaluation_v88 import build_diverse_cases


def example():
    return {
        "id": "external-B1-001", "cefr": "B1", "objective": "Independent German exercise",
        "exercise": {"type": "translation", "answer": "Obwohl es regnet, gehe ich spazieren."},
        "learner_answer": "Obwohl es regnet, gehe ich spazieren.",
        "source": "external_human_authored_pending_verification", "split": "holdout",
        "human_review": {"status": "pending"},
    }


class HoldoutPipelineTests(unittest.TestCase):
    def test_valid_external_row_has_no_structural_errors(self):
        self.assertEqual(check_holdout([example()]), [])

    def test_development_content_leak_is_blocked(self):
        dev = build_diverse_cases()[0]
        row = example()
        row.update({"objective": dev["objective"], "exercise": dev["exercise"],
                    "learner_answer": dev["learner_answer"]})
        self.assertIn("external-B1-001:duplicate_content", check_holdout([row]))

    def test_duplicate_ids_and_invalid_split_blocked(self):
        first, second = example(), example()
        second["split"] = "development"
        errors = check_holdout([first, second])
        self.assertIn("external-B1-001:duplicate_id", errors)
        self.assertIn("external-B1-001:not_holdout", errors)

    def test_unverified_source_is_blocked(self):
        row = example()
        row["source"] = "curated_author_written_unreviewed"
        self.assertIn("external-B1-001:unverified_source", check_holdout([row]))

    def test_import_and_report_stay_blocked_without_reviews(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "holdout.jsonl"
            path.write_text(json.dumps(example(), ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertEqual(len(load_holdout(path)), 1)
            report = evaluate_file(path)
            self.assertEqual(report["release_gate"], "blocked")
            self.assertIn("B1:independent_holdout_insufficient", report["failed_gates"])


if __name__ == "__main__":
    unittest.main()
