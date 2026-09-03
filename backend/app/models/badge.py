# backend/app/models/badge.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class UserBadge(Base):
    __tablename__ = 'user_badges'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    badge_type = Column(String(50), nullable=False)
    badge_name = Column(String(100), nullable=False)
    badge_icon = Column(String(10), nullable=False)
    earned_at = Column(DateTime, server_default=func.now())

