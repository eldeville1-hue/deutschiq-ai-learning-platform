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
from app.models.beta import BetaAcceptanceCheck, BetaEnrollment, BetaInvite
from app.services.beta_acceptance import ACCEPTANCE_CATALOG, acceptance_report
from app.services.beta_insights import beta_readiness, exercise_health, lesson_content_health, retention_cohorts, summarize_events, tester_progress
from app.services.bot_links import telegram_beta_invite_url
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.content_quality import curriculum_journey_issues, normalize_lesson_content, publication_blockers

router = APIRouter(prefix="/api/internal", tags=["internal"])


def require_control_key(x_control_key: str = Header(default="")) -> None:
    if not settings.TASK_SECRET or not compare_digest(x_control_key, settings.TASK_SECRET):
        raise HTTPException(status_code=403, detail="Invalid control-center key")


class InviteRequest(BaseModel):
    label: str = Field(default="Beta invite", min_length=1, max_length=80)
    max_uses: int = Field(default=1, ge=1, le=500)


class InviteBatchRequest(BaseModel):
    label_prefix: str = Field(default="Beta tester", min_length=1, max_length=64)
    count: int = Field(default=15, ge=1, le=50)


class AcceptanceUpdate(BaseModel):
    passed: bool
    notes: str = Field(default="", max_length=500)


@router.get("/curriculum", dependencies=[Depends(require_control_key)])
async def curriculum_preview_catalog(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.is_active == True).all()

    def order(item: Lesson):
        content = item.content if isinstance(item.content, dict) else {}
        return (item.level, int(content.get("day") or 999), item.id)

    result = []
    for item in sorted(lessons, key=order):
        content = item.content or {}
        blockers = publication_blockers(content) if int(content.get("quality_version") or 0) >= 8 else ["quality:legacy_version"]
        result.append({
            "id": item.id,
            "level": item.level,
            "pillar": item.pillar,
            "topic": item.topic,
            "day": int(content.get("day") or 0),
            "module": int(content.get("module") or content.get("week") or 0),
            "title": content.get("title") or item.topic,
            "quality_version": int(content.get("quality_version") or 0),
            "exercise_count": len(content.get("exercises") or []),
            "publish_ready": not blockers,
            "publication_blockers": blockers,
            "reviewed_languages": sorted(language for language, status in ((content.get("content_review") or {}).get("languages") or {}).items() if status == "reviewed"),
            "delayed_review_method": (content.get("delayed_review") or {}).get("method"),
        })
    return result


@router.get("/curriculum/{lesson_id}", dependencies=[Depends(require_control_key)])
async def curriculum_preview_lesson(
    lesson_id: int,
    lang: str = Query(default="ru", pattern="^(ru|de|en)$"),
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.is_active == True).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    content = localize_lesson_content(
        normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level),
        normalize_language(lang),
    )
    return {
        "id": lesson.id,
        "level": lesson.level,
        "pillar": lesson.pillar,
        "topic": lesson.topic,
        "estimated_time": lesson.estimated_time,
        "xp_reward": lesson.xp_reward,
        "content": content,
        "publish_ready": not publication_blockers(lesson.content or {}),
        "publication_blockers": publication_blockers(lesson.content or {}),
        "preview": True,
    }


@router.post("/invites", dependencies=[Depends(require_control_key)])
async def create_invite(payload: InviteRequest, db: Session = Depends(get_db)):
    code = secrets.token_hex(4).upper()
    invite = BetaInvite(code=code, label=payload.label, max_uses=payload.max_uses)
    db.add(invite); db.commit(); db.refresh(invite)
    return {"id": invite.id, "code": invite.code, "label": invite.label, "max_uses": invite.max_uses, "uses": invite.uses, "active": invite.active}


@router.post("/invites/batch", dependencies=[Depends(require_control_key)])
async def create_invite_batch(payload: InviteBatchRequest, db: Session = Depends(get_db)):
    invites = []
    for index in range(payload.count):
        invite = BetaInvite(code=secrets.token_hex(4).upper(), label=f"{payload.label_prefix} {index + 1:02d}", max_uses=1)
        db.add(invite)
        invites.append(invite)
    db.commit()
    for invite in invites:
        db.refresh(invite)
    return {"created": len(invites), "invites": [{"id": item.id, "code": item.code, "label": item.label, "max_uses": 1, "uses": 0, "active": True, "invite_url": telegram_beta_invite_url(settings.TELEGRAM_BOT_USERNAME, item.code)} for item in invites]}


@router.delete("/invites/{invite_id}", dependencies=[Depends(require_control_key)])
async def deactivate_invite(invite_id: int, db: Session = Depends(get_db)):
    invite = db.query(BetaInvite).filter(BetaInvite.id == invite_id).first()
    if not invite: raise HTTPException(status_code=404, detail="Invite not found")
    invite.active = False; db.commit()
    return {"ok": True}


@router.put("/acceptance/{check_id}", dependencies=[Depends(require_control_key)])
async def update_acceptance_check(check_id: str, payload: AcceptanceUpdate, db: Session = Depends(get_db)):
    valid_ids = {item[0] for item in ACCEPTANCE_CATALOG}
    if check_id not in valid_ids:
        raise HTTPException(status_code=404, detail="Unknown acceptance check")
    check = db.query(BetaAcceptanceCheck).filter(BetaAcceptanceCheck.check_id == check_id).first()
    if not check:
        check = BetaAcceptanceCheck(check_id=check_id)
        db.add(check)
    check.passed = payload.passed
    check.notes = payload.notes.strip() or None
    db.commit()
    db.refresh(check)
    return {"id": check.check_id, "passed": check.passed, "notes": check.notes or "", "updated_at": check.updated_at.isoformat() if check.updated_at else None}


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
    acceptance = acceptance_report(db.query(BetaAcceptanceCheck).all())
    event_summary = summarize_events(events)
    all_sessions = db.query(LearningSession).all()
    session_users = {item.user_id for item in sessions}
    completed_sessions = [item for item in sessions if item.status in {"passed", "practice_needed"}]
    started_count = event_summary["unique_users"].get("lesson_started", 0)
    completed_count = event_summary["unique_users"].get("lesson_completed", 0)
    languages = {}
    for user in users:
        language = user.language_code or "unknown"
        languages[language] = languages.get(language, 0) + 1
    a1_lessons = [item for item in lessons if item.is_active and item.level == "A1"]
    content_health = lesson_content_health(a1_lessons, attempts, sessions, events, publication_blockers)
    journey_issues = curriculum_journey_issues(a1_lessons)
    curriculum_readiness = []
    expected_counts = {"A1": 20, "A2": 20, "B1": 24, "B2": 16}
    for level, expected in expected_counts.items():
        track_lessons = [item for item in lessons if item.is_active and item.level == level]
        blocked = [item for item in track_lessons if publication_blockers(item.content or {})]
        if level in {"A1", "A2"}:
            issues = curriculum_journey_issues(track_lessons, expected)
        elif level == "B1":
            issues = curriculum_journey_issues(track_lessons, expected, list(range(31, 55)), [36, 42, 48, 54])
        else:
            issues = []
        curriculum_readiness.append({
            "level": level,
            "lessons": len(track_lessons),
            "expected_lessons": expected,
            "publish_ready_lessons": len(track_lessons) - len(blocked),
            "journey_issues": issues,
            "ready": len(track_lessons) == expected and not blocked and not issues,
        })
    readiness = beta_readiness(content_health, event_summary, len(enrollments), len(session_users), journey_issues, acceptance)
    return {
        "window_days": days,
        "generated_at": datetime.now().isoformat(),
        "curriculum_readiness": curriculum_readiness,
        "audience": {
            "total_users": len(users),
            "new_users": sum(1 for item in users if item.created_at and item.created_at.replace(tzinfo=None) >= since),
            "active_learners": len(session_users),
            "languages": languages,
        },
        "funnel": {
            "invite_claimed": event_summary["unique_users"].get("invite_claimed", len(enrollments)),
            "onboarding_completed": event_summary["unique_users"].get("beta_onboarding_completed", sum(1 for item in enrollments if item.consent and item.goal)),
            "diagnostic_started": event_summary["unique_users"].get("diagnostic_started", 0),
            "diagnostic_completed": event_summary["unique_users"].get("diagnostic_completed", sum(1 for item in users if item.diagnostic_completed)),
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
        "content_health": content_health,
        "readiness": readiness,
        "retention": retention_cohorts(enrollments, all_sessions, datetime.now()),
        "acceptance": acceptance,
        "beta": {
            "enrolled": len(enrollments),
            "onboarded": sum(1 for item in enrollments if item.consent and item.goal),
            "invites": [{"id": item.id, "code": item.code, "label": item.label, "uses": item.uses, "max_uses": item.max_uses, "active": item.active} for item in invites],
        },
        "testers": tester_progress(enrollments, users, invites, all_sessions, events, settings.SECRET_KEY),
    }
