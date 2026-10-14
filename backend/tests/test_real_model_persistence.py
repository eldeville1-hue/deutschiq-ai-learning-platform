"""Persistence contract using DeutschIQ's real ORM models and an isolated DB.

SQLite is used only for this test; the real PostgreSQL ARRAY review_dates
column is not written or read here. No production credentials are needed.
"""
from sqlalchemy import Column, Integer, Table, create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.user import User
from app.models.progress import UserProgress
from app.models.learning import LearningSession


def test_real_models_survive_reopening_database_session(tmp_path):
    # A minimal lessons table satisfies foreign keys without the unrelated
    # PostgreSQL-only ARRAY columns on the production Lesson model.
    lessons = Table("lessons", Base.metadata, Column("id", Integer, primary_key=True), extend_existing=True)
    engine = create_engine(f"sqlite:///{tmp_path / 'real_models.sqlite'}")
    Base.metadata.create_all(engine, tables=[User.__table__, lessons, UserProgress.__table__, LearningSession.__table__])
    Session = sessionmaker(bind=engine)

    with Session() as db:
        user = User(telegram_id=987654321, current_level="B1", xp=75, streak=2)
        db.add(user)
        db.flush()
        user_id = user.id
        db.execute(lessons.insert().values(id=42))
        db.add(UserProgress(user_id=user_id, lesson_id=42, completed=True, score=100))
        db.add(LearningSession(id="persistence-test-session", user_id=user_id, lesson_id=42, status="passed", score=100))
        db.commit()

    with Session() as db:
        user = db.query(User).filter_by(telegram_id=987654321).one()
        progress = db.query(UserProgress).filter_by(user_id=user.id, lesson_id=42).one()
        session = db.query(LearningSession).filter_by(id="persistence-test-session").one()
        assert (user.current_level, user.xp, user.streak) == ("B1", 75, 2)
        assert progress.completed is True
        assert progress.score == 100
        assert session.status == "passed"
        assert session.score == 100
    engine.dispose()
