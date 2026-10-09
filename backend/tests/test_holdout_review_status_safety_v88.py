import unittest

from tests.holdout_pipeline_v88 import check_holdout


class HoldoutReviewStatusSafetyV88Tests(unittest.TestCase):
    def row(self, status):
        return {
            "id": "external-unique-001", "cefr": "A1", "objective": "External review objective",
            "exercise": {"type": "translation", "answer": "Der Mond ist heute wunderbar hell."},
            "learner_answer": "Heute ist der Mond hell.", "source": "external_teacher_casebook",
            "split": "holdout", "human_review": {"status": status},
        }

    def test_unknown_review_status_is_rejected(self):
        errors = check_holdout([self.row("verified")], development=[])
        self.assertIn("external-unique-001:invalid_review_status", errors)

    def test_missing_review_status_is_rejected(self):
        errors = check_holdout([self.row(None)], development=[])
        self.assertIn("external-unique-001:invalid_review_status", errors)

    def test_pending_review_status_does_not_forge_approval(self):
        errors = check_holdout([self.row("pending")], development=[])
        self.assertNotIn("external-unique-001:invalid_review_status", errors)

    def test_self_claimed_approval_still_requires_provenance(self):
        errors = check_holdout([self.row("approved")], development=[])
        self.assertIn("external-unique-001:approved_review_missing_provenance", errors)


if __name__ == "__main__":
    unittest.main()
