"""PostgreSQL learner-row lock contract used by lesson answer writes.

Uses an isolated temporary-named table in TEST_POSTGRES_URL and drops it
afterwards. This verifies PostgreSQL locking behavior, not the entire API race.
"""
import os
import unittest
from uuid import uuid4

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


@unittest.skipUnless(os.environ.get("TEST_POSTGRES_URL"), "TEST_POSTGRES_URL is required")
class PostgresLearnerRowLockTests(unittest.TestCase):
    def test_same_learner_serializes_writes_without_blocking_other_learner(self):
        engine = create_engine(os.environ["TEST_POSTGRES_URL"])
        table = "test_learner_lock_" + uuid4().hex
        try:
            self.assertEqual("postgresql", engine.dialect.name)
            with engine.begin() as setup:
                setup.execute(text(f"CREATE TABLE {table} (id integer PRIMARY KEY)"))
                setup.execute(text(f"INSERT INTO {table} (id) VALUES (1), (2)"))
            with engine.connect() as first, engine.connect() as second:
                with first.begin():
                    first.execute(text(f"SELECT id FROM {table} WHERE id = 1 FOR UPDATE"))
                    # NOWAIT turns a blocked concurrent answer into a
                    # deterministic failure instead of hanging the CI job.
                    with second.begin():
                        second.execute(text("SAVEPOINT before_locked_row"))
                        with self.assertRaises(OperationalError) as locked:
                            second.execute(text(f"SELECT id FROM {table} WHERE id = 1 FOR UPDATE NOWAIT"))
                        self.assertEqual("55P03", locked.exception.orig.sqlstate)
                        second.execute(text("ROLLBACK TO SAVEPOINT before_locked_row"))
                        self.assertEqual(2, second.scalar(text(
                            f"SELECT id FROM {table} WHERE id = 2 FOR UPDATE NOWAIT"
                        )))
                with second.begin():
                    self.assertEqual(1, second.scalar(text(
                        f"SELECT id FROM {table} WHERE id = 1 FOR UPDATE NOWAIT"
                    )))
        finally:
            with engine.begin() as cleanup:
                cleanup.execute(text(f"DROP TABLE IF EXISTS {table}"))
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
