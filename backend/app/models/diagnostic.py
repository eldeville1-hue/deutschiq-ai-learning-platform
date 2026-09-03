from sqlalchemy import Column, Integer, Float, JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func
from .base import Base

class DiagnosticResult(Base):
    __tablename__ = 'diagnostic_results'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    overall_score = Column(Float)
    grammar_score = Column(Float)
    vocabulary_score = Column(Float)
    listening_score = Column(Float)
    pronunciation_score = Column(Float)
    weak_points = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

class DiagnosticMistake(Base):
    __tablename__ = 'diagnostic_mistakes'
    id = Column(Integer, primary_key=True, index=True)
    diagnostic_id = Column(Integer, ForeignKey('diagnostic_results.id', ondelete='CASCADE'), nullable=False, index=True)
    topic = Column(String(80), nullable=False)
    question = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, default='')
