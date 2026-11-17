"""Two simultaneous lesson answer submissions against isolated PostgreSQL tables.

Requires TEST_POSTGRES_URL. This exercises the real check_answer endpoint
function with independent SQLAlchemy sessions, not an HTTP transport test.
"""
import asyncio
import os
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.api.endpoints.lesson import CheckAnswerRequest, StartLessonRequest, check_answer, start_lesson
from app.models.learning import ExerciseAttempt, LearningSession, TopicMastery
from app.models.lesson import Lesson
from app.models.user import User


@unittest.skipUnless(os.environ.get("TEST_POSTGRES_URL"), "TEST_POSTGRES_URL is required")
class ConcurrentPostgresAnswerTests(unittest.TestCase):
    def test_two_simultaneous_correct_answers_credit_once(self):
        schema = "test_answer_race_" + uuid4().hex
        admin = create_engine(os.environ["TEST_POSTGRES_URL"])
        engine = None
        try:
            self.assertEqual("postgresql", admin.dialect.name)
            with admin.begin() as connection:
                connection.execute(text(f"CREATE SCHEMA {schema}"))
            engine = create_engine(
                os.environ["TEST_POSTGRES_URL"],
                connect_args={"options": f"-csearch_path={schema}"},
                pool_size=3, max_overflow=2,
            )
            # Only the endpoint's required tables; all FK targets are present.
            for model in (User, Lesson, LearningSession, ExerciseAttempt, TopicMastery):
                model.__table__.create(engine, checkfirst=True)
            with Session(engine) as db:
                db.add(User(telegram_id=991177))
                db.add(Lesson(
                    id=991177, level="B1", pillar="grammar", topic="connectors",
                    weak_point_tags=[], content={"exercises": [{
                        "type": "choose", "question": "Choose a conjunction.",
                        "answer": "obwohl", "accepted_answers": ["obwohl"],
                        "options": ["weil", "obwohl"],
                    }]},
                ))
                db.commit()
                started = asyncio.run(start_lesson(
                    StartLessonRequest(user_id=991177, lesson_id=991177),
                    db=db, authenticated_id=991177,
                ))
            barrier = threading.Barrier(2, timeout=15)
            from app.api.endpoints import lesson as lesson_module
            original_evaluate = lesson_module.evaluate_structured_answer

            def synchronized_evaluation(*args, **kwargs):
                result = original_evaluate(*args, **kwargs)
                barrier.wait()
                return result

            def submit():
                with Session(engine) as db:
                    try:
                        result = asyncio.run(check_answer(
                            CheckAnswerRequest(
                                user_id=991177, lesson_id=991177,
                                session_id=started["session_id"], exercise_index=0,
                                answer="obwohl", confidence="sure",
                            ),
                            db=db, authenticated_id=991177,
                        ))
                        return ("ok", result["correct"])
                    except HTTPException as error:
                        db.rollback()
                        return ("http", error.status_code)

            with patch.object(lesson_module, "evaluate_structured_answer", synchronized_evaluation):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    first = pool.submit(submit)
                    second = pool.submit(submit)
                    results = [first.result(timeout=30), second.result(timeout=30)]
            self.assertCountEqual([("ok", True), ("http", 409)], results)
            with Session(engine) as db:
                owner = db.query(User).filter_by(telegram_id=991177).one()
                self.assertEqual(1, db.query(ExerciseAttempt).filter_by(user_id=owner.id).count())
                mastery = db.query(TopicMastery).filter_by(user_id=owner.id, topic="connectors").one()
                self.assertEqual(1, mastery.attempts)
                self.assertEqual(1, mastery.correct_total)
        finally:
            if engine is not None:
                engine.dispose()
            with admin.begin() as connection:
                connection.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
            admin.dispose()


if __name__ == "__main__":
    unittest.main()
