from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.event import ProductEvent
from app.models.user import User

router = APIRouter(prefix="/api/events", tags=["events"])

ALLOWED_EVENTS = {
    "dashboard_viewed", "lesson_started", "exercise_answered",
    "lesson_completed", "review_started", "tutor_opened",
    "review_completed", "exercise_retried", "lesson_stage_viewed", "lesson_abandoned",
    "session_finished", "beta_feedback", "level_unlocked", "app_started",
    "reload_loop_detected", "api_failed", "api_slow", "client_error",
    "microphone_failed", "draft_restored", "checkpoint_draft_restored",
    "invite_claimed", "beta_onboarding_completed", "diagnostic_started",
    "diagnostic_completed",
}


class EventRequest(BaseModel):
    user_id: int
    event_name: str
    properties: dict = Field(default_factory=dict)


@router.post("", status_code=204)
async def capture_event(data: EventRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    if data.event_name not in ALLOWED_EVENTS:
        raise HTTPException(status_code=422, detail="Unknown event")
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    safe_properties = {
        str(key)[:48]: (value[:800] if isinstance(value, str) else value)
        for key, value in list(data.properties.items())[:12]
        if isinstance(value, (str, int, float, bool))
    }
    db.add(ProductEvent(user_id=user.id, event_name=data.event_name, properties=safe_properties))
    db.commit()
    return Response(status_code=204)
