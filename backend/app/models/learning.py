from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.sql import func
from .base import Base


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), index=True, nullable=False)
    session_id = Column(String(36), ForeignKey("learning_sessions.id", ondelete="CASCADE"), index=True, nullable=True)
    exercise_index = Column(Integer, nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    answer = Column(String, nullable=False)
    correct = Column(Boolean, nullable=False)
    confidence = Column(String(12), nullable=True)
    response_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TopicMastery(Base):
    __tablename__ = "topic_mastery"
    __table_args__ = (UniqueConstraint("user_id", "topic", name="uq_topic_mastery_user_topic"),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    mastery = Column(Float, default=0.0, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    correct_streak = Column(Integer, default=0, nullable=False)
    correct_total = Column(Integer, default=0, nullable=False)
    lapse_count = Column(Integer, default=0, nullable=False)
    stability_days = Column(Float, default=1.0, nullable=False)
    last_answer_at = Column(DateTime(timezone=True), nullable=True)
    next_review_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class LearningSession(Base):
    __tablename__ = "learning_sessions"
    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(String(20), default="active", nullable=False)
    score = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class SpeechUsage(Base):
    __tablename__ = "speech_usage"
    __table_args__ = (UniqueConstraint("user_id", "usage_date", name="uq_speech_usage_user_date"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    usage_date = Column(String(10), index=True, nullable=False)
    requests_used = Column(Integer, default=0, nullable=False)
    audio_bytes = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SpeechAttempt(Base):
    __tablename__ = "speech_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), index=True, nullable=True)
    modality = Column(String(16), index=True, nullable=False)
    match_score = Column(Integer, nullable=True)
    recognized_words = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
