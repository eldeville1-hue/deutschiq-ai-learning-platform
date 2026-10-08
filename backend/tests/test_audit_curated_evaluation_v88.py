import unittest
from tests.audit_curated_evaluation_v88 import audit, triage
from tests.generate_curated_evaluation_v88 import build_diverse_cases

class CuratedAuditTests(unittest.TestCase):
    def test_curated_dataset_is_structurally_consistent(self):
        report = audit()
        self.assertEqual(report["total"], 480)
        self.assertEqual(report["structural_issues"], [])
        self.assertEqual(report["levels"], {"A1": 120, "A2": 120, "B1": 120, "B2": 120})
        self.assertEqual(report["families"], {"translation": 400, "error_repair": 80})
        self.assertFalse(report["independently_validated"])
        self.assertEqual(report["release_gate"], "blocked")

    def test_triage_prioritizes_potential_false_acceptance(self):
        rows = build_diverse_cases()[:3]
        def accept_everything(answer, exercise):
            return {"evaluation_status": "verified", "correct": True, "errors": []}
        report = triage(rows, evaluator=accept_everything)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["cases"][0]["issue"], "potential_false_accept")
        self.assertEqual(report["cases"][0]["priority"], 0)
        self.assertTrue(report["cases"][0]["review_required"])
        self.assertEqual(report["release_gate"], "blocked")
        self.assertFalse(report["independently_validated"])

    def test_triage_deferral_is_not_false_acceptance(self):
        rows = build_diverse_cases()[:3]
        def defer(answer, exercise):
            return {"evaluation_status": "uncertain", "correct": False, "errors": []}
        report = triage(rows, evaluator=defer)
        self.assertNotIn("potential_false_accept", report["by_issue"])
        self.assertIn("deferred_incorrect", report["by_issue"])

    def test_duplicate_ids_are_detected(self):
        rows = build_diverse_cases()
        rows[1]["id"] = rows[0]["id"]
        self.assertIn("missing_or_duplicate_id", [x["issue"] for x in audit(rows)["structural_issues"]])

    def test_wrong_provisional_correct_label_is_detected(self):
        rows = build_diverse_cases()
        rows[2]["provisional_expected"] = "correct"
        self.assertIn("correct_not_in_accepted_answers", [x["issue"] for x in audit(rows)["structural_issues"]])

    def test_reviewed_or_holdout_case_cannot_be_mislabeled_curated_development(self):
        rows = build_diverse_cases()
        rows[0]["split"] = "holdout"
        rows[0]["human_review"]["status"] = "approved"
        issues = {x["issue"] for x in audit(rows)["structural_issues"]}
        self.assertIn("curated_fixture_must_not_be_holdout", issues)
        self.assertIn("curated_fixture_must_remain_unreviewed", issues)

if __name__ == "__main__":
    unittest.main()
