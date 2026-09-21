from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.models.user import User
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.learning import TopicMastery
from app.services.answer_intelligence import evaluate_structured_answer
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.learning_route import next_cefr_track, normalize_cefr

router = APIRouter(prefix="/api/checkpoint", tags=["checkpoint"])

def checkpoint_lessons(db: Session, level: str):
    lessons = [item for item in db.query(Lesson).filter(Lesson.is_active == True).all() if isinstance(item.content, dict) and item.content.get("track") == level]
    lessons.sort(key=lambda item: int((item.content or {}).get("day") or 999))
    if not lessons:
        return []
    step = max(1, len(lessons) // 8)
    return lessons[::step][:8]

def eligibility(db: Session, user: User, level: str) -> dict:
    lessons = [item for item in db.query(Lesson).filter(Lesson.is_active == True).all() if isinstance(item.content, dict) and item.content.get("track") == level]
    ids = [item.id for item in lessons]
    completed = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id.in_(ids), UserProgress.completed == True).count() if ids else 0
    topics = {item.topic for item in lessons}
    values = [float(row.mastery or 0) for row in db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all() if row.topic in topics]
    completion = round(completed / len(lessons) * 100) if lessons else 0
    mastery = round(sum(values) / len(values)) if values else 0
    return {"eligible": completion >= 80 and mastery >= 70, "completion": completion, "mastery": mastery}

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
        exercise = next((item for item in content.get("exercises", []) if item.get("type") in {"error_repair", "context_choice", "listening_choice"}), None)
        if not exercise:
            continue
        items.append({"id": index, "lesson_id": lesson.id, "topic": lesson.topic, "question": exercise.get("question"), "options": exercise.get("options") or []})
    return {"level": level, "pass_score": 75, "items": items}

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
        exercise = next((item for item in content.get("exercises", []) if item.get("type") in {"error_repair", "context_choice", "listening_choice"}), {})
        result = evaluate_structured_answer(data.answers[index] if index < len(data.answers) else "", exercise)
        results.append({"correct": result["correct"], "topic": lesson.topic, "correct_answer": result["model"], "missing_words": result["missing_words"]})
    score = round(sum(1 for item in results if item["correct"]) / max(len(results), 1) * 100)
    passed = score >= 75
    unlocked = next_cefr_track(level) if passed else None
    if unlocked:
        user.current_level = unlocked
        db.commit()
    return {"passed": passed, "score": score, "required": 75, "unlocked_level": unlocked, "results": results}
