from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.diagnostic import DiagnosticResult
from app.models.learning import TopicMastery
from app.models.progress import UserProgress
from app.models.user import User

router = APIRouter(prefix="/api/user-data", tags=["privacy"])


def _user(db: Session, telegram_id: int) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}")
async def export_data(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = _user(db, user_id)
    diagnostics = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).all()
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all()
    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).all()
    return {
        "profile": {"telegram_id": user.telegram_id, "language": user.language_code, "level": user.current_level, "target_level": user.target_level, "xp": user.xp, "streak": user.streak, "created_at": user.created_at},
        "diagnostics": [{"score": item.overall_score, "weak_points": item.weak_points, "created_at": item.created_at} for item in diagnostics],
        "mastery": [{"topic": item.topic, "mastery": item.mastery, "attempts": item.attempts, "next_review_at": item.next_review_at} for item in mastery],
        "lesson_progress": [{"lesson_id": item.lesson_id, "completed": item.completed, "score": item.score} for item in progress],
    }


@router.delete("/{user_id}", status_code=204)
async def delete_data(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = _user(db, user_id)
    db.delete(user)
    db.commit()
    return Response(status_code=204)
