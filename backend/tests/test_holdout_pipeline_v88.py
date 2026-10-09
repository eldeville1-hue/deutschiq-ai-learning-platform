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

    def test_same_substantial_reference_answer_is_not_independent_coverage(self):
        first = example()
        second = example()
        second["id"] = "external-B1-002"
        second["objective"] = "Different learning objective"
        second["learner_answer"] = "Obwohl es regnet, gehe ich nicht spazieren."
        errors = check_holdout([first, second], development=[])
        self.assertIn(
            "external-B1-002:duplicate_reference_answer:external-B1-001", errors
        )

    def test_short_generic_reference_is_not_automatically_duplicate(self):
        first = example()
        first["exercise"]["answer"] = "Ja."
        second = example()
        second["id"] = "external-B1-002"
        second["objective"] = "Another objective"
        second["learner_answer"] = "Nein."
        second["exercise"]["answer"] = "Ja."
        errors = check_holdout([first, second], development=[])
        self.assertNotIn(
            "external-B1-002:duplicate_reference_answer:external-B1-001", errors
        )

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

    def test_claimed_approval_without_provenance_is_rejected(self):
        row = example()
        row["human_review"] = {"status": "approved", "decision": "correct"}
        self.assertIn("external-B1-001:approved_review_missing_provenance", check_holdout([row]))

    def test_unverified_independence_is_rejected(self):
        row = example()
        row["human_review"] = {
            "status": "approved", "decision": "correct", "reviewer": "human",
            "reviewed_at": "2026-10-08", "protocol_version": "v88-1",
            "blind_to_prediction": True, "independent_of_generation": False,
        }
        self.assertIn("external-B1-001:review_independence_not_verified", check_holdout([row]))

    def test_incorrect_review_needs_error_diagnosis(self):
        row = example()
        row["human_review"] = {
            "status": "approved", "decision": "incorrect", "reviewer": "human",
            "reviewed_at": "2026-10-08", "protocol_version": "v88-1",
            "blind_to_prediction": True, "independent_of_generation": True,
        }
        self.assertIn("external-B1-001:missing_error_diagnosis", check_holdout([row]))

    def test_import_and_report_stay_blocked_without_reviews(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "holdout.jsonl"
            path.write_text(json.dumps(example(), ensure_ascii=False) + "\n", encoding="utf-8")
            self.assertEqual(len(load_holdout(path)), 1)
            report = evaluate_file(path)
            self.assertEqual(report["release_gate"], "blocked")
            self.assertIn("holdout_reviews_incomplete", report["failed_gates"])
            self.assertEqual(report["pending_review_total"], 1)
            self.assertNotIn("levels", report)


if __name__ == "__main__":
    unittest.main()
