from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    telegram_invoice_id = Column(String(50), unique=True)
    amount = Column(Integer)
    currency = Column(String(3), default='XTR')
    status = Column(String(20), default='pending')
    plan_type = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

