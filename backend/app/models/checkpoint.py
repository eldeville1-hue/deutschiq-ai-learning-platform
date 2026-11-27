from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.sql import func

from .base import Base


class CheckpointReceipt(Base):
    __tablename__ = "checkpoint_receipts"
    __table_args__ = (UniqueConstraint("user_id", "attempt_id", name="uq_checkpoint_receipt_user_attempt"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    attempt_id = Column(String(64), nullable=False)
    request_hash = Column(String(64), nullable=False)
    response = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
