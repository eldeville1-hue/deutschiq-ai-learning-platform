from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.sql import func
from .base import Base


class BetaInvite(Base):
    __tablename__ = "beta_invites"
    id = Column(Integer, primary_key=True)
    code = Column(String(32), unique=True, index=True, nullable=False)
    label = Column(String(80), nullable=False, default="Beta")
    max_uses = Column(Integer, nullable=False, default=10)
    uses = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BetaEnrollment(Base):
    __tablename__ = "beta_enrollments"
    __table_args__ = (UniqueConstraint("user_id", name="uq_beta_enrollment_user"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    invite_id = Column(Integer, ForeignKey("beta_invites.id", ondelete="SET NULL"), nullable=True)
    goal = Column(String(40), nullable=True)
    study_minutes = Column(Integer, nullable=True)
    consent = Column(Boolean, nullable=False, default=False)
    status = Column(String(20), nullable=False, default="active")
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

