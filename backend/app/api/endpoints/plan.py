# backend/app/api/endpoints/plan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plan import generate_plan
from app.models.user import User
from app.models.progress import UserProgress
from app.models.learning import TopicMastery
import traceback
from sqlalchemy.exc import SQLAlchemyError
from app.core.telegram_auth import telegram_user_id, assert_owner

router = APIRouter(prefix="/api/plan", tags=["plan"])

@router.get("/{user_id}")
async def get_plan(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            return {"error": f"Пользователь с telegram_id {user_id} не найден"}
        lessons = generate_plan(db, user.id)
        completed_ids = {
            row[0] for row in db.query(UserProgress.lesson_id).filter(
                UserProgress.user_id == user.id,
                UserProgress.completed == True,
            ).all()
        }
        mastery_rows = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all()
        mastery = {row.topic: round(row.mastery) for row in mastery_rows}
        week_titles = {
            1: "Satzbau",
            2: "Dativ & Akkusativ",
            3: "Der, Die, Das",
            4: "Perfekt",
        }
        return [{
            "id": lesson.id,
            "day": (lesson.content or {}).get("day", index + 1),
            "week": (lesson.content or {}).get("week", min(index // 7 + 1, 4)),
            "week_title": week_titles.get((lesson.content or {}).get("week", min(index // 7 + 1, 4)), "Wiederholung"),
            "topic": lesson.topic,
            "pillar": lesson.pillar,
            "level": lesson.level,
            "estimated_time": lesson.estimated_time,
            "completed": lesson.id in completed_ids,
            "mastery": mastery.get(lesson.topic),
        } for index, lesson in enumerate(lessons)]
    except SQLAlchemyError:
        db.rollback()
        return []
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
