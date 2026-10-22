"""Wrong-answer feedback must not congratulate learners for incorrect work."""
import asyncio
import unittest
from unittest.mock import MagicMock, patch

from app.api.endpoints.lesson import CheckAnswerRequest, check_answer
from app.models.learning import LearningSession
from app.models.lesson import Lesson
from app.models.user import User


class IncorrectFeedbackCopyTests(unittest.TestCase):
    def test_wrong_answer_never_uses_success_fallback(self):
        user = User(id=1, telegram_id=123456)
        lesson = Lesson(id=1, level="A1", pillar="grammar", topic="articles",
                        content={"exercises": [{"type": "multiple_choice", "question": "Choose",
                                                 "options": ["ist", "sind"], "answer": "ist"}]})
        session = LearningSession(id="session", user_id=1, lesson_id=1, status="active")
        db = MagicMock()
        db.query.return_value.filter.return_value.first.side_effect = [
            lesson, user, session, None, None, None, None,
        ]
        db.query.return_value.filter.return_value.count.return_value = 0
        db.get_bind.return_value.dialect.name = "sqlite"
        with patch("app.api.endpoints.lesson.evaluate_structured_answer",
                   return_value={"correct": False, "evaluation_status": "verified",
                                 "error_type": "articles", "errors": []}), \
             patch("app.api.endpoints.lesson.normalize_lesson_content",
                   return_value={"exercises": [{"type": "multiple_choice", "answer": "ist"}]}), \
             patch("app.api.endpoints.lesson.localize_lesson_content",
                   side_effect=lambda value, language: value), \
             patch("app.api.endpoints.lesson.skill_for") as skill, \
             patch("app.api.endpoints.lesson.misconception_feedback", return_value="Check the verb form."), \
             patch("app.api.endpoints.lesson.supported_retry_exercise", return_value=None):
            skill.return_value.pillar = "grammar"
            result = asyncio.run(check_answer(
                CheckAnswerRequest(user_id=123456, lesson_id=1, exercise_index=0,
                                   answer="sind", session_id="session", language="en"),
                db=db, authenticated_id=123456,
            ))
        self.assertFalse(result["correct"])
        self.assertEqual("Check the verb form.", result["explanation"])
        self.assertNotIn("form and meaning fit", result["explanation"].lower())


if __name__ == "__main__":
    unittest.main()
