"""Real PostgreSQL regression: concurrent correct answers must count only once.

Uses an isolated temporary schema in CI's TEST_POSTGRES_URL, never production.
"""
import asyncio
import os
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CheckAnswerRequest, check_answer
from app.models.user import User
from app.models.lesson import Lesson
from app.models.learning import LearningSession, ExerciseAttempt, TopicMastery


@unittest.skipUnless(os.getenv("TEST_POSTGRES_URL"), "Requires isolated CI PostgreSQL")
class ConcurrentAnswerPostgresTests(unittest.TestCase):
    def setUp(self):
        self.schema = "answer_test_" + uuid.uuid4().hex[:16]
        self.admin = create_engine(os.environ["TEST_POSTGRES_URL"])
        with self.admin.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA "{self.schema}"'))
        self.engine = create_engine(
            os.environ["TEST_POSTGRES_URL"],
            connect_args={"options": f"-csearch_path={self.schema}"},
            pool_size=4,
        )
        for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.add_all([
                User(id=1, telegram_id=991234),
                Lesson(id=12, level="A1", pillar="grammar", topic="articles",
                       weak_point_tags=[], content={"exercises": [
                           {"type": "multiple_choice", "question": "Choose",
                            "options": ["ist", "sind"], "answer": "ist"}
                       ]}),
                LearningSession(id="concurrent-answer", user_id=1, lesson_id=12, status="active"),
            ])
            db.commit()

    def tearDown(self):
        self.engine.dispose()
        with self.admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{self.schema}" CASCADE'))
        self.admin.dispose()

    def test_simultaneous_correct_submissions_update_mastery_once(self):
        barrier = Barrier(2)

        def submit():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                try:
                    return asyncio.run(check_answer(
                        CheckAnswerRequest(
                            user_id=991234, lesson_id=12, exercise_index=0,
                            answer="ist", session_id="concurrent-answer", language="en",
                        ),
                        db=db, authenticated_id=991234,
                    ))
                except HTTPException as exc:
                    return exc.status_code

        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(submit)
            second = pool.submit(submit)
            results = [first.result(timeout=30), second.result(timeout=30)]

        self.assertEqual(1, sum(isinstance(result, dict) and result.get("correct") is True for result in results))
        self.assertEqual(1, results.count(409))
        with Session(self.engine) as db:
            attempts = db.query(ExerciseAttempt).all()
            self.assertEqual(1, len(attempts))
            self.assertTrue(attempts[0].correct)
            mastery = db.query(TopicMastery).one()
            self.assertEqual(1, mastery.attempts)
            self.assertEqual(1, mastery.correct_total)


if __name__ == "__main__":
    unittest.main()
