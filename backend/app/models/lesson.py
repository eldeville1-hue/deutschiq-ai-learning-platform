from sqlalchemy import Column, Integer, String, JSON, Boolean, ARRAY
from .base import Base

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(3), nullable=False)
    pillar = Column(String(20), nullable=False)
    topic = Column(String(100), nullable=False)
    weak_point_tags = Column(ARRAY(String), nullable=False)
    content = Column(JSON, nullable=False)
    xp_reward = Column(Integer, default=50)
    estimated_time = Column(Integer, default=15)
    is_active = Column(Boolean, default=True)

