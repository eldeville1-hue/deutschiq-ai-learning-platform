# backend/app/api/endpoints/badges.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.badge import UserBadge
from app.core.telegram_auth import telegram_user_id, assert_owner

router = APIRouter(prefix="/api/badges", tags=["badges"])

@router.get("/{user_id}")
async def get_badges(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    badges = db.query(UserBadge).filter(UserBadge.user_id == user.id).all()
    return [
        {"badge_type": b.badge_type, "badge_name": b.badge_name, "badge_icon": b.badge_icon, "earned_at": b.earned_at}
        for b in badges
    ]
