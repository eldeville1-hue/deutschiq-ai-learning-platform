import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.api.endpoints.tutor import save_exchange


class TutorVerifiedEventTests(unittest.TestCase):
    def test_verified_attempt_is_logged_without_changing_mastery(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        usage = SimpleNamespace(questions_used=0)
        with patch("app.api.endpoints.tutor.update_practice_session"):
            response = save_exchange(
                db, 42, "Ich heute lerne Deutsch.", "Try again.",
                usage, 3, "verified_drill", "en",
                verified_result={"topic": "word_order", "correct": False, "attempt_number": 2},
            )
        events = [call.args[0] for call in db.add.call_args_list
                  if getattr(call.args[0], "event_name", None) == "tutor_verified_attempt"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].properties["topic"], "word_order")
        self.assertFalse(events[0].properties["correct"])
        self.assertEqual(events[0].properties["attempt_number"], 2)
        self.assertNotIn("answer", events[0].properties)
        self.assertEqual(response["remaining"], 2)
        db.commit.assert_called_once()

    def test_unverified_chat_does_not_create_verified_attempt(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        usage = SimpleNamespace(questions_used=0)
        with patch("app.api.endpoints.tutor.update_practice_session"):
            save_exchange(db, 42, "Explain Genitiv", "Rule.", usage, 3, "ai", "en")
        self.assertFalse(any(
            getattr(call.args[0], "event_name", None) == "tutor_verified_attempt"
            for call in db.add.call_args_list
        ))


if __name__ == "__main__":
    unittest.main()
