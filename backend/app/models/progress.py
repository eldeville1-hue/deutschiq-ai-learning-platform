from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, ARRAY
from sqlalchemy.sql import func
from .base import Base

class UserProgress(Base):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete="CASCADE"))
    completed = Column(Boolean, default=False)
    score = Column(Float, nullable=True)
    review_dates = Column(ARRAY(DateTime), default=[])
    completed_at = Column(DateTime, nullable=True)

