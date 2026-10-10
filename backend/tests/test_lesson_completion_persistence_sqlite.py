"""SQLite regression for lesson completion, progress, and XP awards."""
import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import ARRAY, JSON, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CompleteLessonRequest, complete_lesson
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class LessonCompletionPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        UserProgress.__table__.c.review_dates.type = JSON()
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery, UserProgress):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001, xp=0, current_level="A2"),
            User(id=2, telegram_id=9002, xp=0, current_level="A2"),
            Lesson(id=10, level="A2", pillar="grammar", topic="articles",
                   weak_point_tags="", xp_reward=50,
                   content={"exercises": [{"type": "choose", "answer": "der"}]}),
            LearningSession(id="learner-one", user_id=1, lesson_id=10, status="active"),
            LearningSession(id="learner-two", user_id=2, lesson_id=10, status="active"),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def complete(self, session_id="learner-one", user_id=9001, authenticated_id=None):
        with patch("app.api.endpoints.lesson.schedule_review"):
            return asyncio.run(complete_lesson(
                CompleteLessonRequest(user_id=user_id, lesson_id=10, session_id=session_id),
                db=self.db, authenticated_id=authenticated_id or user_id,
            ))

    def test_passed_lesson_persists_progress_and_awards_xp_once(self):
        self.db.add(ExerciseAttempt(
            user_id=1, lesson_id=10, session_id="learner-one",
            exercise_index=0, topic="articles", answer="der", correct=True,
        ))
        self.db.commit()
        result = self.complete()
        self.assertTrue(result["passed"])
        self.assertEqual(50, result["xp_gained"])
        self.db.expire_all()
        self.assertEqual(50, self.db.get(User, 1).xp)
        self.assertTrue(self.db.query(UserProgress).filter_by(user_id=1, lesson_id=10).one().completed)
        self.assertEqual("passed", self.db.get(LearningSession, "learner-one").status)
        with self.assertRaises(HTTPException) as error:
            self.complete()
        self.assertEqual(409, error.exception.status_code)
        self.assertEqual(50, self.db.get(User, 1).xp)
        self.assertEqual(1, self.db.query(UserProgress).filter_by(user_id=1, lesson_id=10).count())

    def test_no_answers_do_not_grant_xp_or_completion(self):
        result = self.complete()
        self.assertFalse(result["passed"])
        self.assertEqual(0, result["xp_gained"])
        self.db.expire_all()
        self.assertEqual(0, self.db.get(User, 1).xp)
        self.assertFalse(self.db.query(UserProgress).filter_by(user_id=1, lesson_id=10).one().completed)

    def test_foreign_session_cannot_complete_or_grant_xp(self):
        with self.assertRaises(HTTPException) as error:
            self.complete(session_id="learner-two")
        self.assertEqual(409, error.exception.status_code)
        self.assertEqual(0, self.db.get(User, 1).xp)
        self.assertEqual(0, self.db.query(UserProgress).count())


if __name__ == "__main__":
    unittest.main()
