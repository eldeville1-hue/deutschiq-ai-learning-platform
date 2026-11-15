"""PostgreSQL regression for concurrent diagnostic retries.

Uses a temporary schema in TEST_POSTGRES_URL, never production.
"""
import asyncio
import os
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.api.endpoints.diagnostic import SubmitAnswers, submit_diagnostic
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult
from app.models.event import ProductEvent
from app.models.user import User


@unittest.skipUnless(os.getenv("TEST_POSTGRES_URL"), "Requires isolated CI PostgreSQL")
class ConcurrentDiagnosticPostgresTests(unittest.TestCase):
    def setUp(self):
        self.schema = "diagnostic_test_" + uuid.uuid4().hex[:16]
        self.admin = create_engine(os.environ["TEST_POSTGRES_URL"])
        with self.admin.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA "{self.schema}"'))
        self.engine = create_engine(
            os.environ["TEST_POSTGRES_URL"],
            connect_args={"options": f"-csearch_path={self.schema}"},
            pool_size=4,
        )
        for model in (User, DiagnosticResult, DiagnosticMistake, ProductEvent):
            model.__table__.create(self.engine, checkfirst=True)
        with Session(self.engine) as db:
            db.add(User(id=1, telegram_id=991235))
            db.commit()

    def tearDown(self):
        self.engine.dispose()
        with self.admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{self.schema}" CASCADE'))
        self.admin.dispose()

    def test_two_simultaneous_retries_create_one_result(self):
        barrier = Barrier(2)
        payload = SubmitAnswers(
            user_id=991235, answers={1: "habe", 2: "Der"},
            language="en", attempt_id="simultaneous-diagnostic-991235",
        )

        def submit():
            with Session(self.engine) as db:
                barrier.wait(timeout=10)
                return asyncio.run(submit_diagnostic(
                    payload, db=db, authenticated_id=991235,
                ))

        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(submit)
            second = pool.submit(submit)
            results = [first.result(timeout=30), second.result(timeout=30)]

        self.assertTrue(all(item["persisted"] for item in results))
        self.assertEqual(results[0]["level"], results[1]["level"])
        with Session(self.engine) as db:
            self.assertEqual(1, db.query(DiagnosticResult).count())
            self.assertEqual(1, db.query(DiagnosticMistake).count())
            self.assertEqual(1, db.query(ProductEvent).filter_by(
                event_name="diagnostic_completed").count())


if __name__ == "__main__":
    unittest.main()
