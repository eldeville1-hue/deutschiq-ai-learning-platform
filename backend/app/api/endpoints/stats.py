# backend/app/api/endpoints/stats.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.progress import UserProgress
from app.core.telegram_auth import telegram_user_id, assert_owner

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/{user_id}")
async def get_user_stats(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    lessons_completed = db.query(UserProgress).filter(
        UserProgress.user_id == user.id,
        UserProgress.completed == True
    ).count()
    
    level_order = ['A1', 'A2', 'B1', 'B2', 'C1']
    current_level = user.current_level or 'A1'
    try:
        next_level = level_order[level_order.index(current_level) + 1]
    except (ValueError, IndexError):
        next_level = 'C1'
    
    xp_needed = 500 - (user.xp % 500) if user.xp % 500 != 0 else 0
    
    locked_badges = [
        {'name': 'Неделя усилий', 'icon': '🔥', 'requirement': '7 дней подряд'},
        {'name': 'Уровень B1', 'icon': '🏆', 'requirement': 'Достигнуть уровня B1'},
        {'name': '50 уроков', 'icon': '🎓', 'requirement': 'Пройти 50 уроков'},
        {'name': 'Месяц усердия', 'icon': '⭐', 'requirement': '30 дней подряд'},
    ]
    
    return {
        'level': current_level,
        'next_level': next_level,
        'xp': user.xp or 0,
        'xp_needed': xp_needed,
        'streak': user.streak or 0,
        'lessons_completed': lessons_completed,
        'total_lessons': 50,
        'subscription_status': user.subscription_status,
        'locked_badges': locked_badges,
    }
