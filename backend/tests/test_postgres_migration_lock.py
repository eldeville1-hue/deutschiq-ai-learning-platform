"""Integration check for transaction-scoped PostgreSQL migration lock.

Set TEST_POSTGRES_URL to an isolated PostgreSQL database to run this test.
No schema changes are made.
"""
import os
import unittest
from sqlalchemy import create_engine, text

LOCK_ID = 8820261015


@unittest.skipUnless(os.environ.get("TEST_POSTGRES_URL"), "TEST_POSTGRES_URL is required")
class PostgresMigrationLockTests(unittest.TestCase):
    """Check the exact advisory-lock key used by migrations/env.py."""
    def test_second_connection_cannot_acquire_lock_until_first_commits(self):
        engine = create_engine(os.environ["TEST_POSTGRES_URL"])
        try:
            if engine.dialect.name != "postgresql":
                self.fail("TEST_POSTGRES_URL must point to PostgreSQL")
            with engine.connect() as first, engine.connect() as second:
                with first.begin():
                    first.execute(text("SELECT pg_advisory_xact_lock(:id)"), {"id": LOCK_ID})
                    with second.begin():
                        blocked = second.scalar(text("SELECT pg_try_advisory_xact_lock(:id)"), {"id": LOCK_ID})
                        self.assertFalse(blocked)
                with second.begin():
                    acquired = second.scalar(text("SELECT pg_try_advisory_xact_lock(:id)"), {"id": LOCK_ID})
                    self.assertTrue(acquired)
        finally:
            engine.dispose()

    def test_rollback_releases_lock(self):
        engine = create_engine(os.environ["TEST_POSTGRES_URL"])
        try:
            with engine.connect() as first, engine.connect() as second:
                transaction = first.begin()
                try:
                    first.execute(text("SELECT pg_advisory_xact_lock(:id)"), {"id": LOCK_ID})
                    with second.begin():
                        self.assertFalse(second.scalar(text("SELECT pg_try_advisory_xact_lock(:id)"), {"id": LOCK_ID}))
                finally:
                    transaction.rollback()
                with second.begin():
                    self.assertTrue(second.scalar(text("SELECT pg_try_advisory_xact_lock(:id)"), {"id": LOCK_ID}))
        finally:
            engine.dispose()


if __name__ == "__main__":
    unittest.main()
