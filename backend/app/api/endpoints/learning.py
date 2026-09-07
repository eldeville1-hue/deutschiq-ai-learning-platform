from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.learning import TopicMastery
from app.models.lesson import Lesson
from app.models.user import User
from app.services.learning_engine import retention_score
from app.services.plan import generate_plan
from app.services.skill_graph import blocked_by, skill_for
from app.services.content_quality import normalize_lesson_content

router = APIRouter(prefix="/api/learning", tags=["learning"])


def _days_overdue(review_at, now: datetime) -> float:
    if not review_at:
        return 0.0
    if review_at.tzinfo is None:
        review_at = review_at.replace(tzinfo=timezone.utc)
    return max(0.0, (now - review_at).total_seconds() / 86_400)


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
    mastery_map = {item.topic: item.mastery for item in mastery}
    plan = generate_plan(db, user.id, limit=10)
    next_lesson = next((item for item in plan if not blocked_by(item.topic, mastery_map)), plan[0] if plan else None)
    due_count = len(due)
    review_count = min(5, due_count)
    phases = []
    if review_count:
        phases.append({"kind": "review", "count": review_count, "minutes": max(2, review_count * 2), "reason": "due"})
    if next_lesson:
        phases.append({
            "kind": "learn",
            "count": 1,
            "minutes": next_lesson.estimated_time or 12,
            "lesson_id": next_lesson.id,
            "topic": next_lesson.topic,
            "reason": "weakest_ready_skill" if mastery else "first_step",
            "prerequisites": list(skill_for(next_lesson.topic).prerequisites),
        })
        phases.append({"kind": "transfer", "count": 1, "minutes": 3, "topic": next_lesson.topic, "reason": "active_use"})
    total_minutes = sum(item["minutes"] for item in phases)
    return {
        "due_count": due_count,
        "due_topics": [{"topic": item.topic, "mastery": round(item.mastery), "retention": retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now))} for item in due[:5]],
        "mastery": [{
            "topic": item.topic,
            "mastery": round(item.mastery),
            "retention": retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now)),
            "attempts": item.attempts,
            "lapses": item.lapse_count or 0,
        } for item in mastery[:8]],
        "next_lesson": ({
            "id": next_lesson.id,
            "topic": next_lesson.topic,
            "level": next_lesson.level,
            "minutes": next_lesson.estimated_time or 12,
            "reason": "review_due" if next_lesson.topic in {item.topic for item in due} else ("weakest_ready_skill" if mastery else "first_step"),
            "blocked_by": blocked_by(next_lesson.topic, mastery_map),
        } if next_lesson else None),
        "session": {
            "phases": phases,
            "minutes": total_minutes,
            "explanation": "review_then_learn" if review_count else "learn_then_transfer",
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
