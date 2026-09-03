# backend/app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from sqlalchemy.exc import SQLAlchemyError
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.models.progress import UserProgress
from app.models.lesson import Lesson

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

def next_cefr(level: str) -> str:
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    try:
        return levels[min(levels.index(level) + 1, len(levels) - 1)]
    except ValueError:
        return "A2"

def level_progress(score: float, level: str) -> int:
    bands = {"A1": (0, 55), "A2": (55, 70), "B1": (70, 85), "B2": (85, 95), "C1": (95, 100)}
    low, high = bands.get(level, (0, 100))
    return max(0, min(100, round((score - low) / max(high - low, 1) * 100)))

@router.get("/{user_id}")
async def get_dashboard(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    fallback = {
        "level": "A1",
        "percentage": 0,
        "targetLevel": "A2",
        "targetProgress": 0,
        "stats": [],
        "weaknesses": [],
        "subscription_status": "free",
        "database_available": False,
        "diagnostic_completed": False,
    }
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
    except SQLAlchemyError:
        db.rollback()
        return fallback
    if not user:
        return fallback
    
    diag = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
    if not diag:
        # Заглушка, если диагностика не пройдена
        return {
            "level": "A1",
            "percentage": 0,
            "targetLevel": "B2",
            "targetProgress": 0,
            "stats": [
                {"label": "grammar", "value": 0, "has_data": False},
                {"label": "pronunciation", "value": 0, "has_data": False},
                {"label": "vocabulary", "value": 0, "has_data": False},
                {"label": "listening", "value": 0, "has_data": False},
            ],
            "weaknesses": [],
            "subscription_status": user.subscription_status,
            "database_available": True,
            "diagnostic_completed": False,
        }
    
    completed_lessons = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.completed == True).count()
    total_lessons = db.query(Lesson).filter(Lesson.level == user.current_level).count()
    plan_progress = round(completed_lessons / total_lessons * 100) if total_lessons else 0
    return {
        "level": user.current_level,
        "percentage": diag.overall_score,
        "diagnostic_score": diag.overall_score,
        "targetLevel": next_cefr(user.current_level),
        "targetProgress": level_progress(diag.overall_score, user.current_level),
        "level_progress": level_progress(diag.overall_score, user.current_level),
        "plan_progress": plan_progress,
        "confidence": "medium",
        "stats": [
            {"label": "grammar", "value": diag.grammar_score, "has_data": True},
            {"label": "pronunciation", "value": 0, "has_data": False},
            {"label": "vocabulary", "value": diag.vocabulary_score, "has_data": True},
            {"label": "listening", "value": 0, "has_data": False},
        ],
        "weaknesses": [{"name": k, "percent": v * 10} for k, v in diag.weak_points.items()][:3] if diag.weak_points else [],
        "subscription_status": user.subscription_status,
        "xp": user.xp or 0,
        "streak": user.streak or 0,
        "database_available": True,
        "diagnostic_completed": bool(user.diagnostic_completed or diag is not None),
    }
