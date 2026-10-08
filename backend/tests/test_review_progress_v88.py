import unittest
from tests.review_evaluation_benchmark import review_progress
from tests.generate_curated_evaluation_v88 import build_diverse_cases


class ReviewProgressTests(unittest.TestCase):
    def test_unreviewed_curated_cases_do_not_count(self):
        report = review_progress(build_diverse_cases())
        for level in ("A1", "A2", "B1", "B2"):
            self.assertEqual(report["levels"][level]["total"], 120)
            self.assertEqual(report["levels"][level]["approved_independent"], 0)
            self.assertEqual(report["levels"][level]["remaining_to_minimum"], 100)
        self.assertEqual(report["release_gate"], "blocked")

    def test_unverified_claims_do_not_count(self):
        rows = build_diverse_cases()[:1]
        rows[0]["human_review"] = {"status": "pending_independence_verification",
                                    "independent_of_generation": True, "blind_to_prediction": True}
        self.assertEqual(review_progress(rows)["levels"]["A1"]["approved_independent"], 0)

    def test_only_explicit_approved_independent_review_counts(self):
        rows = build_diverse_cases()[:1]
        rows[0]["human_review"] = {"status": "approved", "independent_of_generation": True,
                                    "blind_to_prediction": True}
        self.assertEqual(review_progress(rows)["levels"]["A1"]["approved_independent"], 1)


if __name__ == "__main__":
    unittest.main()
