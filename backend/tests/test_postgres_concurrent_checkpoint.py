"""Concurrent B1 graduation on isolated CI PostgreSQL."""
import asyncio
import os
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.api.endpoints.checkpoint import CheckpointSubmission, submit_checkpoint
from app.models.user import User
from app.models.lesson import Lesson
from app.models.event import ProductEvent
from app.models.checkpoint import CheckpointReceipt


@unittest.skipUnless(os.getenv("TEST_POSTGRES_URL"), "Requires isolated CI PostgreSQL")
class ConcurrentCheckpointPostgresTests(unittest.TestCase):
    def setUp(self):
        self.schema = "checkpoint_test_" + uuid.uuid4().hex[:16]
        self.admin = create_engine(os.environ["TEST_POSTGRES_URL"])
        with self.admin.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA "{self.schema}"'))
        self.engine = create_engine(os.environ["TEST_POSTGRES_URL"],
            connect_args={"options": f"-csearch_path={self.schema} -clock_timeout=10000"})
        for model in (User, Lesson, ProductEvent, CheckpointReceipt):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.add_all([
                User(id=1, telegram_id=991236, current_level="B1"),
                User(id=2, telegram_id=991237, current_level="B1"),
                Lesson(id=77, level="B1", pillar="grammar", topic="connectors",
                       weak_point_tags=[], is_active=True,
                       content={"track": "B1", "day": 1, "exercises": [
                           {"type": "dialogue", "mission_role": "final", "question": "Explain your plans."}]}),
            ])
            db.commit()

    def tearDown(self):
        self.engine.dispose()
        with self.admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{self.schema}" CASCADE'))
        self.admin.dispose()

    def test_simultaneous_passing_submissions_graduate_once(self):
        barrier = Barrier(2)

        async def evaluate(*args):
            await asyncio.sleep(0.25)
            return {"correct": True, "score": 90,
                    "dimension_scores": {"task_completion": 95, "grammar": 90},
                    "feedback": "Good answer", "improvement": ""}

        def submit():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                try:
                    result = asyncio.run(submit_checkpoint(
                        CheckpointSubmission(user_id=991236, level="B1",
                            answers=["Ich möchte studieren, weil ich gern lerne."]),
                        db=db, authenticated_id=991236))
                    return result["unlocked_level"]
                except HTTPException as error:
                    return error.status_code

        with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}), \
             patch("app.api.endpoints.checkpoint.evaluate_production",
                   new_callable=AsyncMock, side_effect=evaluate) as scorer:
            with ThreadPoolExecutor(max_workers=2) as pool:
                first, second = pool.submit(submit), pool.submit(submit)
                results = [first.result(timeout=30), second.result(timeout=30)]
            self.assertCountEqual(["B2", 403], results)
            self.assertEqual(1, scorer.await_count)
        with Session(self.engine) as db:
            self.assertEqual("B2", db.query(User).filter_by(id=1).one().current_level)
            self.assertEqual("B1", db.query(User).filter_by(id=2).one().current_level)
            self.assertEqual(1, db.query(ProductEvent).filter_by(
                user_id=1, event_name="checkpoint_completed").count())

    def test_simultaneous_same_attempt_replays_once(self):
        barrier = Barrier(2)

        async def evaluate(*args):
            await asyncio.sleep(0.25)
            return {"correct": True, "score": 90,
                    "dimension_scores": {"task_completion": 95, "grammar": 90},
                    "feedback": "Good answer", "improvement": ""}

        def submit():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                try:
                    result = asyncio.run(submit_checkpoint(
                        CheckpointSubmission(user_id=991236, level="B1",
                            answers=["Ich möchte studieren, weil ich gern lerne."], attempt_id="same-attempt"),
                        db=db, authenticated_id=991236))
                    return result
                except HTTPException as error:
                    return error.status_code

        with patch("app.api.endpoints.checkpoint.eligibility", return_value={"eligible": True}), \
             patch("app.api.endpoints.checkpoint.evaluate_production",
                   new_callable=AsyncMock, side_effect=evaluate) as scorer:
            with ThreadPoolExecutor(max_workers=2) as pool:
                first, second = pool.submit(submit), pool.submit(submit)
                results = [first.result(timeout=30), second.result(timeout=30)]
            self.assertEqual(results[0], results[1])
            self.assertEqual("B2", results[0]["unlocked_level"])
            self.assertEqual(1, scorer.await_count)
        with Session(self.engine) as db:
            self.assertEqual("B2", db.query(User).filter_by(id=1).one().current_level)
            self.assertEqual("B1", db.query(User).filter_by(id=2).one().current_level)
            self.assertEqual(1, db.query(ProductEvent).filter_by(
                user_id=1, event_name="checkpoint_completed").count())
            self.assertEqual(1, db.query(CheckpointReceipt).filter_by(user_id=1).count())
