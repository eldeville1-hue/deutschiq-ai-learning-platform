"""Persist the current tutor exercise without confusing chat with verified course mastery."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func
from .base import Base


class TutorPracticeSession(Base):
    __tablename__ = "tutor_practice_sessions"
    __table_args__ = (UniqueConstraint("user_id", "language", name="uq_tutor_practice_user_lang"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    language = Column(String(8), nullable=False)
    exercise_text = Column(Text, nullable=False)
    state = Column(String(24), nullable=False, default="awaiting_attempt")
    attempts = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
