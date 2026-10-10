"""Real SQLite persistence regression for both personalized recommendation handlers."""
import asyncio
import unittest
from unittest.mock import patch

from sqlalchemy import ARRAY, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session

from app.api.endpoints.learning import today
from app.api.endpoints.plan import get_plan
from app.models.diagnostic import DiagnosticResult
from app.models.learning import ExerciseAttempt, TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User


@compiles(ARRAY, "sqlite")
def sqlite_array(_type, _compiler, **kwargs):
    return "TEXT"


class PersistedPersonalizationTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        for model in (User, Lesson, DiagnosticResult, UserProgress, TopicMastery, ExerciseAttempt):
            model.__table__.create(self.engine, checkfirst=True)
        self.db = Session(self.engine)
        self.db.add_all([
            User(id=1, telegram_id=9001, current_level="A2", language_code="en"),
            User(id=2, telegram_id=9002, current_level="A2", language_code="en"),
            Lesson(id=1, level="A2", pillar="grammar", topic="word_order",
                   weak_point_tags="", content={"track": "A2", "day": 1}),
            Lesson(id=2, level="A2", pillar="grammar", topic="articles",
                   weak_point_tags="", content={"track": "A2", "day": 2}),
        ])
        self.db.commit()
        self.db.add_all([
            TopicMastery(user_id=1, topic="word_order", mastery=85, attempts=5),
            TopicMastery(user_id=1, topic="articles", mastery=75, attempts=4),
            ExerciseAttempt(user_id=1, lesson_id=2, exercise_index=0, topic="articles",
                            answer="wrong", correct=False),
            ExerciseAttempt(user_id=1, lesson_id=2, exercise_index=1, topic="articles",
                            answer="wrong", correct=False),
            TopicMastery(user_id=2, topic="word_order", mastery=65, attempts=5),
            TopicMastery(user_id=2, topic="articles", mastery=85, attempts=4),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_both_handlers_read_real_attempt_rows_and_isolate_learners(self):
        route = self.db.query(Lesson).order_by(Lesson.id).all()
        with patch("app.api.endpoints.plan.generate_plan", return_value=route), \
             patch("app.api.endpoints.learning.generate_plan", return_value=route):
            focused_plan = asyncio.run(get_plan(9001, db=self.db, authenticated_id=9001))
            focused_today = asyncio.run(today(9001, db=self.db, authenticated_id=9001))
            other_plan = asyncio.run(get_plan(9002, db=self.db, authenticated_id=9002))
            other_today = asyncio.run(today(9002, db=self.db, authenticated_id=9002))
        self.assertEqual(2, next(item["id"] for item in focused_plan if item["recommended"]))
        self.assertEqual(2, focused_today["next_lesson"]["id"])
        self.assertEqual(1, next(item["id"] for item in other_plan if item["recommended"]))
        self.assertEqual(1, other_today["next_lesson"]["id"])
        self.assertEqual([], focused_today["next_lesson"]["blocked_by"])


if __name__ == "__main__":
    unittest.main()
