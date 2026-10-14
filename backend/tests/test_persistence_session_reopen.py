"""Verify committed learner state survives a new SQLAlchemy session.

This uses an isolated temporary SQLite database; it never touches Supabase.
"""
from sqlalchemy import create_engine, Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Learner(Base):
    __tablename__ = "test_learners"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    xp = Column(Integer, default=0)
    current_level = Column(String(3), default="A1")


class Completion(Base):
    __tablename__ = "test_completions"
    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey("test_learners.id"), nullable=False)
    lesson_id = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)


def test_committed_progress_survives_session_reopen(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'progress.sqlite'}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)

    with Session() as db:
        learner = Learner(telegram_id=123456, xp=0, current_level="A1")
        db.add(learner)
        db.flush()
        db.add(Completion(learner_id=learner.id, lesson_id=42, completed=True))
        learner.xp += 50
        db.commit()

    # A new connection/session simulates a fresh request after app restart.
    with Session() as db:
        learner = db.query(Learner).filter_by(telegram_id=123456).one()
        completion = db.query(Completion).filter_by(learner_id=learner.id, lesson_id=42).one()
        assert learner.xp == 50
        assert learner.current_level == "A1"
        assert completion.completed is True
    engine.dispose()
