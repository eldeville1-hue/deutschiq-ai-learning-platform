"""Real answer verification must survive a fresh DB session after Telegram reload."""
import asyncio
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import (
    CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson,
)
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class VerifiedLessonReopenTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.engine = create_engine(f"sqlite:///{Path(self.temp.name) / 'learner.sqlite'}")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.add(User(id=1, telegram_id=9001))
            db.add(Lesson(
                id=10, level="A2", pillar="grammar", topic="articles",
                weak_point_tags="", content={"exercises": [
                    {"type": "choose", "question": "Which article?", "answer": "der",
                     "accepted_answers": ["der"], "options": ["der", "die"]},
                    {"type": "choose", "question": "Which article now?", "answer": "das",
                     "accepted_answers": ["das"], "options": ["der", "das"]},
                ]},
            ))
            db.commit()

    def tearDown(self):
        self.engine.dispose()
        self.temp.cleanup()

    def start(self, db):
        return asyncio.run(start_lesson(
            StartLessonRequest(user_id=9001, lesson_id=10),
            db=db, authenticated_id=9001,
        ))

    def answer(self, db, session_id, index, value):
        return asyncio.run(check_answer(
            CheckAnswerRequest(
                user_id=9001, lesson_id=10, exercise_index=index,
                answer=value, session_id=session_id,
            ), db=db, authenticated_id=9001,
        ))

    def test_wrong_retry_correct_and_reopen_keep_verified_cursor(self):
        with Session(self.engine) as first_db:
            first = self.start(first_db)
            self.assertFalse(first["resumed"])
            self.assertEqual(0, first["next_exercise_index"])
            self.assertFalse(self.answer(first_db, first["session_id"], 0, "die")["correct"])

        # A new SQLAlchemy session/connection simulates a new Telegram request.
        with Session(self.engine) as reopened_db:
            resumed = self.start(reopened_db)
            self.assertTrue(resumed["resumed"])
            self.assertEqual(first["session_id"], resumed["session_id"])
            self.assertEqual(0, resumed["next_exercise_index"])
            self.assertTrue(self.answer(reopened_db, resumed["session_id"], 0, "der")["correct"])

        with Session(self.engine) as reopened_again:
            resumed = self.start(reopened_again)
            self.assertTrue(resumed["resumed"])
            self.assertEqual(1, resumed["next_exercise_index"])
            attempts = reopened_again.query(ExerciseAttempt).filter_by(user_id=1).order_by(ExerciseAttempt.id).all()
            self.assertEqual([False, True], [row.correct for row in attempts])
            self.assertEqual(1, reopened_again.query(LearningSession).filter_by(user_id=1).count())
            mastery = reopened_again.query(TopicMastery).filter_by(user_id=1, topic="articles").one()
            self.assertEqual(2, mastery.attempts)
            self.assertEqual(1, mastery.correct_total)
            self.assertTrue(self.answer(reopened_again, resumed["session_id"], 1, "das")["correct"])


if __name__ == "__main__":
    unittest.main()
