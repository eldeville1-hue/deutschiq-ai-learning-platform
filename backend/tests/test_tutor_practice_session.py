import unittest
from unittest.mock import MagicMock
from app.models.tutor_practice import TutorPracticeSession
from app.services.tutor_practice_session import update_practice_session


class PracticeSessionTests(unittest.TestCase):
    def test_new_exercise_creates_awaiting_session(self):
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        update_practice_session(db, 7, "en", "Practice please", "Exercise: Put these words in order.")
        db.add.assert_called_once()
        session = db.add.call_args.args[0]
        self.assertEqual(session.state, "awaiting_attempt")
        self.assertEqual(session.attempts, 0)

    def test_attempt_moves_to_feedback_and_increments(self):
        db = MagicMock()
        session = TutorPracticeSession(user_id=7, language="en", exercise_text="Exercise: Put these words in order.", state="awaiting_attempt", attempts=0)
        db.query.return_value.filter.return_value.first.return_value = session
        update_practice_session(db, 7, "en", "Ich lerne heute Deutsch.", "Check your verb position and try again.")
        self.assertEqual(session.state, "feedback_given")
        self.assertEqual(session.attempts, 1)

    def test_new_exercise_resets_attempt_count(self):
        db = MagicMock()
        session = TutorPracticeSession(user_id=7, language="en", exercise_text="Exercise: old task.", state="feedback_given", attempts=2)
        db.query.return_value.filter.return_value.first.return_value = session
        update_practice_session(db, 7, "en", "Next", "Exercise: new sentence.")
        self.assertEqual(session.state, "awaiting_attempt")
        self.assertEqual(session.attempts, 0)

    def test_new_request_interrupts_session(self):
        db = MagicMock()
        session = TutorPracticeSession(user_id=7, language="en", exercise_text="Exercise: old task.", state="awaiting_attempt", attempts=0)
        db.query.return_value.filter.return_value.first.return_value = session
        update_practice_session(db, 7, "en", "Explain Genitiv", "Genitiv expresses possession.")
        self.assertEqual(session.state, "interrupted")


if __name__ == "__main__":
    unittest.main()
