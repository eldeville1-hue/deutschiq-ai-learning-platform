"""SQLite regression for starting, resuming, and isolating learning sessions."""
import asyncio
import unittest

from fastapi import HTTPException
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import StartLessonRequest, start_lesson
from app.models.learning import ExerciseAttempt, LearningSession
from app.models.lesson import Lesson
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class LessonSessionResumeDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001),
            User(id=2, telegram_id=9002),
            Lesson(id=10, level="A2", pillar="grammar", topic="articles", content={}),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def start(self, user_id, resume_session_id=None):
        return asyncio.run(start_lesson(
            StartLessonRequest(user_id=user_id, lesson_id=10,
                               resume_session_id=resume_session_id),
            db=self.db, authenticated_id=user_id,
        ))

    def test_reload_reuses_session_and_advances_only_after_correct_answers(self):
        first = self.start(9001)
        self.assertFalse(first["resumed"])
        self.assertEqual(0, first["next_exercise_index"])
        self.db.add_all([
            ExerciseAttempt(user_id=1, lesson_id=10, session_id=first["session_id"],
                            exercise_index=0, topic="articles", answer="wrong", correct=False),
            ExerciseAttempt(user_id=1, lesson_id=10, session_id=first["session_id"],
                            exercise_index=0, topic="articles", answer="correct", correct=True),
            ExerciseAttempt(user_id=1, lesson_id=10, session_id=first["session_id"],
                            exercise_index=1, topic="articles", answer="wrong", correct=False),
        ])
        self.db.commit()
        resumed = self.start(9001)
        explicit = self.start(9001, resume_session_id=first["session_id"])
        self.assertEqual(first["session_id"], resumed["session_id"])
        self.assertEqual(first["session_id"], explicit["session_id"])
        self.assertTrue(resumed["resumed"])
        self.assertEqual(1, resumed["next_exercise_index"])
        self.assertEqual(1, self.db.query(LearningSession).filter_by(user_id=1).count())

    def test_sessions_are_isolated_between_learners(self):
        first = self.start(9001)
        second = self.start(9002, resume_session_id=first["session_id"])
        self.assertNotEqual(first["session_id"], second["session_id"])
        self.assertFalse(second["resumed"])
        self.assertEqual(2, self.db.query(LearningSession).count())

    def test_cannot_start_session_using_another_telegram_identity(self):
        with self.assertRaises(HTTPException) as error:
            asyncio.run(start_lesson(
                StartLessonRequest(user_id=9002, lesson_id=10),
                db=self.db, authenticated_id=9001,
            ))
        self.assertEqual(403, error.exception.status_code)
        self.assertEqual(0, self.db.query(LearningSession).count())


if __name__ == "__main__":
    unittest.main()
