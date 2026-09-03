from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from app.core.telegram_auth import telegram_user_id, assert_owner

router = APIRouter(prefix="/api/user", tags=["user"])


class LanguageUpdate(BaseModel):
    user_id: int
    language: str


@router.get("/state/{telegram_id}")
async def get_user_state(telegram_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, telegram_id)
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return {
            "exists": False,
            "diagnostic_completed": False,
            "language": "ru",
            "level": "A1",
            "xp": 0,
            "streak": 0,
        }
    diagnostic = (
        db.query(DiagnosticResult)
        .filter(DiagnosticResult.user_id == user.id)
        .order_by(DiagnosticResult.created_at.desc())
        .first()
    )
    return {
        "exists": True,
        "diagnostic_completed": bool(user.diagnostic_completed or diagnostic is not None),
        "language": user.language_code if user.language_code in ("ru", "de") else "ru",
        "level": user.current_level or "A1",
        "xp": user.xp or 0,
        "streak": user.streak or 0,
    }


@router.put("/language")
async def update_language(payload: LanguageUpdate, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, payload.user_id)
    language = payload.language if payload.language in ("ru", "de") else "ru"
    user = db.query(User).filter(User.telegram_id == payload.user_id).first()
    if not user:
        user = User(telegram_id=payload.user_id, language_code=language)
        db.add(user)
    else:
        user.language_code = language
    db.commit()
    return {"language": language}
