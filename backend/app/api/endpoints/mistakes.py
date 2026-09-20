from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.diagnostic import DiagnosticMistake, DiagnosticResult
from app.models.user import User
from app.models.learning import ExerciseAttempt
from app.models.lesson import Lesson
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.content_quality import normalize_lesson_content

router = APIRouter(prefix="/api/mistakes", tags=["mistakes"])


@router.get("/{user_id}")
async def get_mistakes(user_id: int, lang: str | None = None, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    diagnostic = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
    language = normalize_language(lang or user.language_code)
    rows = db.query(DiagnosticMistake).filter(DiagnosticMistake.diagnostic_id == diagnostic.id).order_by(DiagnosticMistake.id).all() if diagnostic else []
    mistakes = [{
        "id": f"diagnostic-{row.id}",
        "source": "diagnostic",
        "topic": row.topic,
        "question": row.question,
        "user_answer": row.user_answer,
        "correct_answer": row.correct_answer,
        "explanation": row.explanation,
    } for row in rows]
    attempts = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id,
    ).order_by(ExerciseAttempt.created_at.desc()).limit(80).all()
    seen = set()
    for attempt in attempts:
        key = (attempt.lesson_id, attempt.exercise_index)
        if key in seen:
            continue
        seen.add(key)
        if attempt.correct:
            continue
        lesson = db.query(Lesson).filter(Lesson.id == attempt.lesson_id).first()
        if not lesson:
            continue
        content = localize_lesson_content(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level), language)
        exercises = content.get("exercises") or []
        if not 0 <= attempt.exercise_index < len(exercises):
            continue
        exercise = exercises[attempt.exercise_index]
        accepted = exercise.get("accepted_answers") or [exercise.get("answer", "")]
        mistakes.append({
            "id": f"lesson-{attempt.id}",
            "source": "lesson",
            "topic": lesson.topic,
            "question": exercise.get("question", ""),
            "user_answer": attempt.answer,
            "correct_answer": accepted[0] if accepted else "",
            "explanation": exercise.get("explanation", ""),
            "lesson_id": lesson.id,
        })
    return {
        "diagnostic_id": diagnostic.id if diagnostic else None,
        "mistakes": mistakes[:24],
    }
