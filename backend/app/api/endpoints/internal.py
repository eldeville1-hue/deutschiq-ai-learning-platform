from datetime import datetime, timedelta
from hmac import compare_digest

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.event import ProductEvent
from app.models.learning import ExerciseAttempt, LearningSession
from app.models.lesson import Lesson
from app.models.user import User
from app.services.beta_insights import exercise_health, summarize_events

router = APIRouter(prefix="/api/internal", tags=["internal"])


def require_control_key(x_control_key: str = Header(default="")) -> None:
    if not settings.TASK_SECRET or not compare_digest(x_control_key, settings.TASK_SECRET):
        raise HTTPException(status_code=403, detail="Invalid control-center key")


@router.get("/beta", dependencies=[Depends(require_control_key)])
async def beta_control_center(
    days: int = Query(default=30, ge=1, le=90),
    db: Session = Depends(get_db),
):
    since = datetime.now() - timedelta(days=days)
    events = db.query(ProductEvent).filter(ProductEvent.created_at >= since).order_by(ProductEvent.created_at.asc()).all()
    attempts = db.query(ExerciseAttempt).filter(ExerciseAttempt.created_at >= since).all()
    sessions = db.query(LearningSession).filter(LearningSession.started_at >= since).all()
    users = db.query(User).all()
    lessons = db.query(Lesson).all()
    event_summary = summarize_events(events)
    session_users = {item.user_id for item in sessions}
    completed_sessions = [item for item in sessions if item.status in {"passed", "practice_needed"}]
    started_count = event_summary["unique_users"].get("lesson_started", 0)
    completed_count = event_summary["unique_users"].get("lesson_completed", 0)
    languages = {}
    for user in users:
        language = user.language_code or "unknown"
        languages[language] = languages.get(language, 0) + 1
    return {
        "window_days": days,
        "generated_at": datetime.now().isoformat(),
        "audience": {
            "total_users": len(users),
            "new_users": sum(1 for item in users if item.created_at and item.created_at.replace(tzinfo=None) >= since),
            "active_learners": len(session_users),
            "languages": languages,
        },
        "funnel": {
            "diagnostic_completed": sum(1 for item in users if item.diagnostic_completed),
            "lesson_started": started_count,
            "lesson_completed": completed_count,
            "completion_rate": round(completed_count / started_count * 100) if started_count else 0,
        },
        "sessions": {
            "started": len(sessions),
            "completed": len(completed_sessions),
            "abandoned_events": event_summary["counts"].get("lesson_abandoned", 0),
        },
        "events": event_summary,
        "exercise_health": exercise_health(attempts, {item.id: item.topic for item in lessons}),
    }
