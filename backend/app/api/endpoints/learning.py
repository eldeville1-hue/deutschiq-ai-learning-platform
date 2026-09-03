from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.learning import TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User
from app.services.content_quality import normalize_lesson_content

router = APIRouter(prefix="/api/learning", tags=["learning"])


@router.get("/today/{user_id}")
async def today(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    due = db.query(TopicMastery).filter(
        TopicMastery.user_id == user.id,
        TopicMastery.next_review_at.isnot(None),
        TopicMastery.next_review_at <= now,
    ).order_by(TopicMastery.mastery.asc()).all()
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).order_by(TopicMastery.mastery.asc()).all()
    return {
        "due_count": len(due),
        "due_topics": [{"topic": item.topic, "mastery": round(item.mastery)} for item in due[:5]],
        "mastery": [{"topic": item.topic, "mastery": round(item.mastery), "attempts": item.attempts} for item in mastery[:8]],
        "session": {
            "learn": 1,
            "practice": 3,
            "review": min(5, len(due)),
            "minutes": 12 + min(5, len(due)) * 2,
        },
    }


@router.get("/reviews/{user_id}")
async def reviews(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    rows = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.next_review_at <= now).order_by(TopicMastery.mastery.asc()).limit(5).all()
    result = []
    for row in rows:
        lesson = db.query(Lesson).filter(Lesson.topic == row.topic, Lesson.is_active == True).first()
        content = normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level) if lesson else {}
        exercises = content.get("exercises", [])
        if lesson and exercises:
            # Повторение проверяет самостоятельное извлечение, а не этап с подсказкой.
            exercise_index = 1 if len(exercises) > 1 else 0
            exercise = exercises[exercise_index]
            result.append({"topic": row.topic, "mastery": round(row.mastery), "lesson_id": lesson.id, "exercise_index": exercise_index, "question": exercise.get("question", ""), "type": exercise.get("type", "fill"), "options": exercise.get("options", []), "tokens": exercise.get("tokens", [])})
    return {"reviews": result}
