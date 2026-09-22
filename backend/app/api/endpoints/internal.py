from datetime import datetime, timedelta
from hmac import compare_digest
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.event import ProductEvent
from app.models.learning import ExerciseAttempt, LearningSession
from app.models.lesson import Lesson
from app.models.user import User
from app.models.beta import BetaEnrollment, BetaInvite
from app.services.beta_insights import exercise_health, retention_cohorts, summarize_events

router = APIRouter(prefix="/api/internal", tags=["internal"])


def require_control_key(x_control_key: str = Header(default="")) -> None:
    if not settings.TASK_SECRET or not compare_digest(x_control_key, settings.TASK_SECRET):
        raise HTTPException(status_code=403, detail="Invalid control-center key")


class InviteRequest(BaseModel):
    label: str = Field(default="Beta invite", min_length=1, max_length=80)
    max_uses: int = Field(default=1, ge=1, le=500)


@router.post("/invites", dependencies=[Depends(require_control_key)])
async def create_invite(payload: InviteRequest, db: Session = Depends(get_db)):
    code = secrets.token_hex(4).upper()
    invite = BetaInvite(code=code, label=payload.label, max_uses=payload.max_uses)
    db.add(invite); db.commit(); db.refresh(invite)
    return {"id": invite.id, "code": invite.code, "label": invite.label, "max_uses": invite.max_uses, "uses": invite.uses, "active": invite.active}


@router.delete("/invites/{invite_id}", dependencies=[Depends(require_control_key)])
async def deactivate_invite(invite_id: int, db: Session = Depends(get_db)):
    invite = db.query(BetaInvite).filter(BetaInvite.id == invite_id).first()
    if not invite: raise HTTPException(status_code=404, detail="Invite not found")
    invite.active = False; db.commit()
    return {"ok": True}


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
    enrollments = db.query(BetaEnrollment).all()
    invites = db.query(BetaInvite).order_by(BetaInvite.created_at.desc()).all()
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
        "retention": retention_cohorts(enrollments, db.query(LearningSession).all(), datetime.now()),
        "beta": {
            "enrolled": len(enrollments),
            "onboarded": sum(1 for item in enrollments if item.consent and item.goal),
            "invites": [{"id": item.id, "code": item.code, "label": item.label, "uses": item.uses, "max_uses": item.max_uses, "active": item.active} for item in invites],
        },
    }
