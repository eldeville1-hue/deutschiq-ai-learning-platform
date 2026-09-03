from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult
from app.models.user import User

router = APIRouter(prefix="/api/mistakes", tags=["mistakes"])


@router.get("/{user_id}")
async def get_mistakes(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    diagnostic = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
    if not diagnostic:
        return {"mistakes": [], "diagnostic_id": None}
    rows = db.query(DiagnosticMistake).filter(DiagnosticMistake.diagnostic_id == diagnostic.id).order_by(DiagnosticMistake.id).all()
    return {
        "diagnostic_id": diagnostic.id,
        "mistakes": [{
            "id": row.id,
            "topic": row.topic,
            "question": row.question,
            "user_answer": row.user_answer,
            "correct_answer": row.correct_answer,
            "explanation": row.explanation,
        } for row in rows],
    }
