import unittest

from tests.holdout_pipeline_v88 import check_holdout


class HoldoutReviewerProvenanceV88Tests(unittest.TestCase):
    def row(self, **review_updates):
        review = {
            "status": "approved", "reviewer": "Independent Reviewer",
            "reviewed_at": "2026-10-09T12:00:00Z", "protocol_version": "v88",
            "decision": "correct", "blind_to_prediction": True,
            "independent_of_generation": True,
        }
        review.update(review_updates)
        return {
            "id": "external-provenance-001", "cefr": "B1",
            "objective": "Independent provenance validation case",
            "exercise": {"type": "translation", "answer": "Der Mond ist heute ungewöhnlich hell."},
            "learner_answer": "Heute scheint der Mond hell.",
            "source": "external_teacher_casebook", "split": "holdout",
            "human_review": review,
        }

    def test_reviewer_identity_must_be_nonempty_text(self):
        for value in (True, 123, "   "):
            with self.subTest(value=value):
                errors = check_holdout([self.row(reviewer=value)], development=[])
                self.assertIn("external-provenance-001:invalid_reviewer_identity", errors)

    def test_review_timestamp_must_be_nonempty_text(self):
        errors = check_holdout([self.row(reviewed_at=True)], development=[])
        self.assertIn("external-provenance-001:invalid_review_timestamp", errors)

    def test_review_timestamp_rejects_invalid_and_future_dates(self):
        for value in ("not-a-date", "2026-10-09T12:00:00", "2999-01-01T00:00:00Z"):
            with self.subTest(value=value):
                errors = check_holdout([self.row(reviewed_at=value)], development=[])
                self.assertIn("external-provenance-001:invalid_review_timestamp", errors)

    def test_review_protocol_must_be_nonempty_text(self):
        errors = check_holdout([self.row(protocol_version=7)], development=[])
        self.assertIn("external-provenance-001:invalid_review_protocol", errors)


if __name__ == "__main__":
    unittest.main()
