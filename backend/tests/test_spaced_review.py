import unittest
from datetime import datetime, timedelta, timezone

from app.services.spaced_review import next_review, review_is_due


class SpacedReviewTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 11, 12, tzinfo=timezone.utc)

    def test_success_advances_intervals_and_caps_at_thirty_days(self):
        state = None
        for interval in (1, 3, 7, 14, 30, 30):
            state = next_review(state, True, self.now)
            self.assertEqual(interval, state["interval_days"])

    def test_error_resets_schedule(self):
        state = next_review({"step": 3}, False, self.now)
        self.assertEqual(0, state["step"])
        self.assertEqual(1, state["interval_days"])

    def test_due_boundary_and_timezone(self):
        state = next_review(None, True, self.now)
        self.assertFalse(review_is_due(state, self.now + timedelta(hours=23)))
        self.assertTrue(review_is_due(state, self.now + timedelta(days=1)))

    def test_invalid_dates_do_not_become_due(self):
        self.assertFalse(review_is_due({"due_at": "not-a-date"}, self.now))
        self.assertFalse(review_is_due({"due_at": "2026-10-11T00:00:00"}, self.now))

    def test_naive_timestamps_and_nonboolean_results_rejected(self):
        with self.assertRaises(ValueError):
            next_review(None, True, datetime(2026, 10, 11))
        with self.assertRaises(ValueError):
            next_review(None, "true", self.now)
        with self.assertRaises(ValueError):
            review_is_due({}, datetime(2026, 10, 11))


if __name__ == "__main__":
    unittest.main()
