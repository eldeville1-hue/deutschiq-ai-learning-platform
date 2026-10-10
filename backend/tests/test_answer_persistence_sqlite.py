"""Persist verified answers and reject foreign sessions (real SQLite)."""
import asyncio
import unittest
from fastapi import HTTPException
from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from app.api.endpoints.lesson import CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User

@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"

class AnswerPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001),
            User(id=2, telegram_id=9002),
            Lesson(id=10, level="A2", pillar="grammar", topic="articles",
                   weak_point_tags="", content={"exercises": [
                       {"type": "choose", "question": "Which article?",
                        "answer": "der", "accepted_answers": ["der"],
                        "explanation": "Masculine nominative."}]}),
        ])
        self.db.commit()
        self.session_id = asyncio.run(start_lesson(
            StartLessonRequest(user_id=9001, lesson_id=10),
            db=self.db, authenticated_id=9001))["session_id"]

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def answer(self, value, session_id=None):
        return asyncio.run(check_answer(
            CheckAnswerRequest(user_id=9001, lesson_id=10, exercise_index=0,
                               answer=value, session_id=session_id or self.session_id),
            db=self.db, authenticated_id=9001))

    def test_wrong_then_correct_answers_persist_and_update_mastery(self):
        self.assertFalse(self.answer("die")["correct"])
        self.assertTrue(self.answer("der")["correct"])
        self.db.expire_all()
        attempts = self.db.query(ExerciseAttempt).filter_by(user_id=1).order_by(ExerciseAttempt.id).all()
        mastery = self.db.query(TopicMastery).filter_by(user_id=1, topic="articles").one()
        self.assertEqual([False, True], [a.correct for a in attempts])
        self.assertEqual(2, mastery.attempts)
        self.assertEqual(1, mastery.correct_total)
        self.assertEqual(1, mastery.correct_streak)

    def test_foreign_session_cannot_mutate_learning_data(self):
        foreign = asyncio.run(start_lesson(
            StartLessonRequest(user_id=9002, lesson_id=10),
            db=self.db, authenticated_id=9002))["session_id"]
        with self.assertRaises(HTTPException) as error:
            self.answer("der", session_id=foreign)
        self.assertEqual(409, error.exception.status_code)
        self.assertEqual(0, self.db.query(ExerciseAttempt).count())
        self.assertEqual(0, self.db.query(TopicMastery).count())

if __name__ == "__main__":
    unittest.main()
