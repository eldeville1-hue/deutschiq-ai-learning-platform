"""Concurrent completion must award XP once on PostgreSQL.

Uses CI TEST_POSTGRES_URL with a temporary schema, never production.
"""
import asyncio
import os
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CompleteLessonRequest, complete_lesson
from app.models.user import User
from app.models.lesson import Lesson
from app.models.learning import LearningSession, ExerciseAttempt, TopicMastery
from app.models.progress import UserProgress


@unittest.skipUnless(os.getenv("TEST_POSTGRES_URL"), "Requires isolated CI PostgreSQL")
class ConcurrentCompletionPostgresTests(unittest.TestCase):
    def setUp(self):
        self.schema = "completion_test_" + uuid.uuid4().hex[:16]
        self.admin = create_engine(os.environ["TEST_POSTGRES_URL"])
        with self.admin.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA "{self.schema}"'))
        self.engine = create_engine(
            os.environ["TEST_POSTGRES_URL"],
            connect_args={"options": f"-csearch_path={self.schema}"},
            pool_size=4,
        )
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery, UserProgress):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.add_all([
                User(id=1, telegram_id=991235, xp=0, current_level="A1"),
                Lesson(id=13, level="A1", pillar="grammar", topic="articles",
                       xp_reward=25, weak_point_tags=[],
                       content={"exercises": [{"type": "multiple_choice", "question": "Choose",
                                              "options": ["ist", "sind"], "answer": "ist"}]}),
            ])
            db.flush()
            db.add(LearningSession(id="concurrent-completion", user_id=1, lesson_id=13, status="active"))
            db.commit()

    def tearDown(self):
        self.engine.dispose()
        with self.admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{self.schema}" CASCADE'))
        self.admin.dispose()

    def test_two_simultaneous_completions_award_xp_once(self):
        barrier = Barrier(2)
        summary = {"score": 100, "first_try_correct": 1, "corrected_retries": 0,
                   "needs_review": 0, "exercise_count": 1}
        mission = {"mission_passed": True, "mission_required": False,
                   "mission_attempted": True, "mission_score": 100, "mission_answer": None}

        def submit():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                return asyncio.run(complete_lesson(
                    CompleteLessonRequest(user_id=991235, lesson_id=13,
                                          session_id="concurrent-completion"),
                    db=db, authenticated_id=991235,
                ))

        with patch("app.api.endpoints.lesson.summarize_attempts", return_value=summary), \
             patch("app.api.endpoints.lesson.summarize_mission", return_value=mission), \
             patch("app.api.endpoints.lesson.schedule_review"):
            with ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(submit)
                second = pool.submit(submit)
                results = [first.result(timeout=30), second.result(timeout=30)]

        self.assertEqual([0, 25], sorted(result["xp_gained"] for result in results))
        self.assertEqual(1, sum(result.get("recovered") is True for result in results))
        with Session(self.engine) as db:
            self.assertEqual(25, db.query(User).one().xp)
            self.assertEqual("passed", db.query(LearningSession).one().status)
            self.assertEqual(1, db.query(UserProgress).count())
            self.assertTrue(db.query(UserProgress).one().completed)


if __name__ == "__main__":
    unittest.main()
