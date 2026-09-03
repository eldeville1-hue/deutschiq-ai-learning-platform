from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from .base import Base


class TutorUsage(Base):
    __tablename__ = "tutor_usage"
    __table_args__ = (UniqueConstraint("user_id", "usage_date", name="uq_tutor_usage_day"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    usage_date = Column(Date, nullable=False, index=True)
    questions_used = Column(Integer, nullable=False, default=0)


class TutorMessage(Base):
    __tablename__ = "tutor_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(16), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
