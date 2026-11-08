"""Verify the retention index is usable for historical learner-topic lookups."""
import sqlite3
import unittest

from app.models.learning import ExerciseAttempt


INDEX_NAME = "ix_exercise_attempts_user_topic_created"


class RetentionIndexQueryPlanTests(unittest.TestCase):
    def test_model_declares_composite_index_in_query_order(self):
        index = next(index for index in ExerciseAttempt.__table__.indexes if index.name == INDEX_NAME)
        self.assertEqual([column.name for column in index.columns], ["user_id", "topic", "created_at"])

    def test_sqlite_uses_index_for_historical_pair_lookup(self):
        connection = sqlite3.connect(":memory:")
        try:
            connection.execute(
                "CREATE TABLE exercise_attempts (id INTEGER PRIMARY KEY, user_id INTEGER, topic TEXT, created_at TEXT)"
            )
            connection.execute(
                f"CREATE INDEX {INDEX_NAME} ON exercise_attempts (user_id, topic, created_at)"
            )
            plan = connection.execute(
                "EXPLAIN QUERY PLAN SELECT * FROM exercise_attempts "
                "WHERE created_at < ? AND (user_id, topic) IN ((?, ?), (?, ?))",
                ("2026-11-01", 1, "weil", 2, "dass"),
            ).fetchall()
            self.assertTrue(
                any(INDEX_NAME in row[3] for row in plan),
                f"Expected retention index in SQLite query plan: {plan}",
            )
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
