"""Read-only PostgreSQL retention index diagnostics.

Run from backend/: python -m scripts.inspect_retention_index
Does not run ANALYZE, mutate data, or print learner identifiers.
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

INDEX_NAME = "ix_exercise_attempts_user_topic_created"


def inspect(connection):
    index = connection.execute(
        text("""
            SELECT indexname FROM pg_indexes
            WHERE schemaname = current_schema()
              AND tablename = 'exercise_attempts'
              AND indexname = :name
        """),
        {"name": INDEX_NAME},
    ).scalar_one_or_none()
    if index is None:
        raise RuntimeError(f"Missing PostgreSQL retention index: {INDEX_NAME}")
    # Use dummy values: EXPLAIN without ANALYZE plans but never executes.
    plan = connection.execute(
        text("""
            EXPLAIN SELECT id FROM exercise_attempts
            WHERE created_at < :cutoff
              AND user_id = :user_id AND topic = :topic
        """),
        {"cutoff": "2026-11-01", "user_id": -1, "topic": "__diagnostic__"},
    ).scalars().all()
    return plan


def main():
    if not settings.DATABASE_URL.startswith("postgresql"):
        raise RuntimeError("PostgreSQL connection required")
    engine = create_engine(settings.DATABASE_URL)
    try:
        with engine.connect() as connection:
            plan = inspect(connection)
        print(f"Index exists: {INDEX_NAME}")
        print("Read-only EXPLAIN (dummy parameters; planner estimate only):")
        for line in plan:
            print(line)
        print("Note: a dummy-value plan does not measure production query latency.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
