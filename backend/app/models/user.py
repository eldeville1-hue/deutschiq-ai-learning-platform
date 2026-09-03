# backend/app/models/user.py
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)  # <-- исправлено!
    language_code = Column(String(2), default='ru')
    current_level = Column(String(3), default='A1')
    target_level = Column(String(3), default='B1')
    subscription_status = Column(String(20), default='free')   # free, pro, premium
    subscription_end_date = Column(DateTime, nullable=True)
    xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    diagnostic_completed = Column(Boolean, nullable=False, default=False, server_default='false')
    last_activity = Column(DateTime, default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
