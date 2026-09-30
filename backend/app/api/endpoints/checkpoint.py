from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.models.user import User
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.learning import ExerciseAttempt, TopicMastery
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.learning_route import next_cefr_track, normalize_cefr
from app.services.assessment_insights import evidence_gate
from app.services.production_feedback import evaluate_production
from app.services.checkpoint_graduation import checkpoint_outcome, final_mission
from app.models.event import ProductEvent

router = APIRouter(prefix="/api/checkpoint", tags=["checkpoint"])

def checkpoint_lessons(db: Session, level: str):
    lessons = [item for item in db.query(Lesson).filter(Lesson.is_active == True).all() if isinstance(item.content, dict) and item.content.get("track") == level]
    lessons.sort(key=lambda item: int((item.content or {}).get("day") or 999))
    if not lessons:
        return []
    # One independent mission from each module is more meaningful than eight
    # recognition questions. Older curricula retain the previous fallback.
    module_missions = [item for item in lessons if (item.content or {}).get("checkpoint")]
    if module_missions:
        return module_missions
    step = max(1, len(lessons) // 4)
    return lessons[::step][:4]


def eligibility(db: Session, user: User, level: str) -> dict:
    lessons = [item for item in db.query(Lesson).filter(Lesson.is_active == True).all() if isinstance(item.content, dict) and item.content.get("track") == level]
    ids = [item.id for item in lessons]
    completed = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id.in_(ids), UserProgress.completed == True).count() if ids else 0
    topics = {item.topic for item in lessons}
    values = [float(row.mastery or 0) for row in db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all() if row.topic in topics]
    completion = round(completed / len(lessons) * 100) if lessons else 0
    mastery = round(sum(values) / len(values)) if values else 0
    attempts = db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == user.id, ExerciseAttempt.topic.in_(topics), ExerciseAttempt.assessment.isnot(None)).order_by(ExerciseAttempt.created_at.desc()).limit(100).all() if topics else []
    evidence = evidence_gate(attempts)
    return {"eligible": completion >= 100 and mastery >= 60 and evidence["eligible"], "completion": completion, "mastery": mastery, "evidence": evidence}

@router.get("/{user_id}/{level}")
async def get_checkpoint(user_id: int, level: str, lang: str = "en", db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    level = normalize_cefr(level)
    if not user or normalize_cefr(user.current_level) != level:
        raise HTTPException(status_code=403, detail="Checkpoint is not available for this level")
    gate = eligibility(db, user, level)
    if not gate["eligible"]:
        raise HTTPException(status_code=403, detail=gate)
    items = []
    for index, lesson in enumerate(checkpoint_lessons(db, level)):
        content = localize_lesson_content(lesson.content or {}, normalize_language(lang))
        exercise = final_mission(content)
        if not exercise:
            continue
        turns = [{
            "partner": turn.get("partner"),
            "goal": turn.get("goal"),
            "placeholder": {"ru": "Ответь самостоятельно по-немецки…", "de": "Antworte selbstständig auf Deutsch…", "en": "Reply independently in German…"}.get(normalize_language(lang), "Reply independently in German…"),
        } for turn in exercise.get("conversation_turns", [])]
        items.append({
            "id": index, "lesson_id": lesson.id, "topic": lesson.topic,
            "type": "dialogue", "stage": "checkpoint", "question": exercise.get("question"),
            "conversation_turns": turns,
        })
    return {"level": level, "pass_score": 70, "format": "independent_missions", "items": items}

class CheckpointSubmission(BaseModel):
    user_id: int
    level: str
    answers: list[str]
    language: str = "en"

@router.post("/submit")
async def submit_checkpoint(data: CheckpointSubmission, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    level = normalize_cefr(data.level)
    if not user or normalize_cefr(user.current_level) != level or not eligibility(db, user, level)["eligible"]:
        raise HTTPException(status_code=403, detail="Checkpoint is not available")
    results = []
    lessons = checkpoint_lessons(db, level)
    for index, lesson in enumerate(lessons):
        content = localize_lesson_content(lesson.content or {}, normalize_language(data.language))
        exercise = final_mission(content)
        result = await evaluate_production(data.answers[index] if index < len(data.answers) else "", exercise, content, normalize_language(data.language))
        results.append({
            "correct": result["correct"], "score": result["score"], "topic": lesson.topic, "lesson_id": lesson.id,
            "dimensions": result["dimension_scores"], "feedback": result["feedback"],
            "improvement": result["improvement"],
        })
    outcome = checkpoint_outcome(results)
    score = outcome["score"]
    dimension_scores = outcome["dimensions"]
    passed = outcome["passed"]
    unlocked = next_cefr_track(level) if passed else None
    if unlocked:
        user.current_level = unlocked
    recovery_topics = list(dict.fromkeys(item["topic"] for item in sorted(results, key=lambda value: value["score"]) if not item["correct"]))[:2]
    recovery_lesson_id = min(results, key=lambda value: value["score"])["lesson_id"] if results and not passed else None
    db.add(ProductEvent(user_id=user.id, event_name="checkpoint_completed", properties={
        "level": level, "passed": passed, "score": score, "unlocked_level": unlocked,
        "dimensions": dimension_scores, "recovery_topics": recovery_topics,
    }))
    db.commit()
    return {
        "passed": passed, "score": score, "required": 70, "unlocked_level": unlocked,
        "completed_level": level if passed else None, "results": results,
        "dimensions": dimension_scores, "recovery_topics": recovery_topics,
        "recovery_lesson_id": recovery_lesson_id,
        "next_route": "new_level" if passed else "repair",
    }
