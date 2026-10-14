"""Regression coverage for the actual spaced-repetition scheduler.

Uses a temporary SQLite database with a JSON type adapter solely for the
PostgreSQL ARRAY(DateTime) field; never connects to production Supabase.
"""
from datetime import datetime, timedelta
from unittest.mock import patch

from sqlalchemy import JSON, Column, Integer, Table, create_engine
from sqlalchemy.orm import Session

from app.models.base import Base
from app.models.user import User
from app.models.progress import UserProgress
from app.services.srs import schedule_review


def test_review_schedule_persists_five_intervals(tmp_path):
    original_type = UserProgress.__table__.c.review_dates.type
    UserProgress.__table__.c.review_dates.type = JSON()
    engine = create_engine(f"sqlite:///{tmp_path / 'srs.sqlite'}")
    try:
        lessons = Table("lessons", Base.metadata, Column("id", Integer, primary_key=True), extend_existing=True)
        Base.metadata.create_all(engine, tables=[User.__table__, lessons, UserProgress.__table__])
        with Session(engine) as db:
            db.add(User(id=1, telegram_id=12345))
            db.execute(lessons.insert().values(id=42))
            db.add(UserProgress(user_id=1, lesson_id=42, completed=True))
            db.commit()

            # JSON is test-only; serialize dates while retaining the scheduler's
            # actual offset and commit behavior.
            real_commit = db.commit
            def commit_serialized_dates():
                for item in db.new.union(db.dirty):
                    if isinstance(item, UserProgress) and item.review_dates:
                        item.review_dates = [
                            value.isoformat() if isinstance(value, datetime) else value
                            for value in item.review_dates
                        ]
                real_commit()

            with patch.object(db, "commit", side_effect=commit_serialized_dates):
                schedule_review(db, 1, 42)

        with Session(engine) as reopened:
            saved = reopened.query(UserProgress).filter_by(user_id=1, lesson_id=42).one()
            assert len(saved.review_dates) == 5
            offsets = [1, 3, 7, 14, 30]
            for raw, offset in zip(saved.review_dates, offsets):
                actual = datetime.fromisoformat(raw)
                assert abs((actual - (datetime.now() + timedelta(days=offset))).total_seconds()) < 30
    finally:
        engine.dispose()
        UserProgress.__table__.c.review_dates.type = original_type


def test_repeated_scheduling_preserves_existing_review_dates(tmp_path):
    """A second scheduler call must not move an existing review plan."""
    original_type = UserProgress.__table__.c.review_dates.type
    UserProgress.__table__.c.review_dates.type = JSON()
    engine = create_engine(f"sqlite:///{tmp_path / 'repeat_srs.sqlite'}")
    try:
        lessons = Table("lessons", Base.metadata, Column("id", Integer, primary_key=True), extend_existing=True)
        Base.metadata.create_all(engine, tables=[User.__table__, lessons, UserProgress.__table__])
        original_dates = [
            (datetime(2026, 10, 15) + timedelta(days=days)).isoformat()
            for days in (0, 2, 6, 13, 29)
        ]
        with Session(engine) as db:
            db.add(User(id=2, telegram_id=23456))
            db.execute(lessons.insert().values(id=43))
            db.add(UserProgress(user_id=2, lesson_id=43, completed=True, review_dates=original_dates))
            db.commit()

        with Session(engine) as db:
            schedule_review(db, 2, 43)
        with Session(engine) as reopened:
            saved = reopened.query(UserProgress).filter_by(user_id=2, lesson_id=43).one()
            assert saved.review_dates == original_dates
    finally:
        engine.dispose()
        UserProgress.__table__.c.review_dates.type = original_type
