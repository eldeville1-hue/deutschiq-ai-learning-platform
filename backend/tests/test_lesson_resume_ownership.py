"""Regression coverage for server-side lesson resume and Telegram ownership."""
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.api.endpoints.lesson import StartLessonRequest, start_lesson


class LessonResumeTests(unittest.TestCase):
    def setUp(self):
        self.user = SimpleNamespace(id=7, telegram_id=12345)
        self.lesson = SimpleNamespace(id=3)
        self.session = SimpleNamespace(id="persisted-session", user_id=7, lesson_id=3, status="active")
        self.db = MagicMock()
        self.db.get_bind.return_value.dialect.name = "sqlite"
        self.db.query.return_value.filter.return_value.first.side_effect = [
            self.user, self.lesson,
        ]
        self.db.query.return_value.filter.return_value.order_by.return_value.first.return_value = self.session
        self.db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
            SimpleNamespace(exercise_index=0, correct=True),
            SimpleNamespace(exercise_index=1, correct=False),
        ]

    def test_reopens_saved_session_at_first_unanswered_exercise(self):
        result = asyncio.run(start_lesson(
            StartLessonRequest(user_id=12345, lesson_id=3),
            db=self.db, authenticated_id=12345,
        ))
        self.assertEqual(result, {
            "session_id": "persisted-session",
            "resumed": True,
            "next_exercise_index": 1,
        })
        self.db.add.assert_not_called()
        self.db.commit.assert_not_called()

    def test_explicit_session_id_cannot_override_telegram_ownership(self):
        with self.assertRaises(HTTPException) as error:
            asyncio.run(start_lesson(
                StartLessonRequest(user_id=12345, lesson_id=3, resume_session_id="persisted-session"),
                db=self.db, authenticated_id=98765,
            ))
        self.assertEqual(error.exception.status_code, 403)
        self.db.query.assert_not_called()


if __name__ == "__main__":
    unittest.main()
