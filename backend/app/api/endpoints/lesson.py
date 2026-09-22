# backend/app/api/endpoints/lesson.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.lesson import Lesson
from app.models.user import User
from app.models.progress import UserProgress
from datetime import datetime, timedelta
import copy
import re
import uuid
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.services.srs import schedule_review
from app.models.learning import ExerciseAttempt, TopicMastery, LearningSession
from app.services.learning_engine import mastery_update, mastery_update_from_evidence, next_stability, review_interval, retention_score, summarize_attempts
from app.services.skill_graph import skill_for
from app.services.content_quality import normalize_lesson_content
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.production_feedback import evaluate_production
from pathlib import Path
from app.services.misconception_feedback import misconception_feedback
from app.services.learning_route import next_cefr_track, normalize_cefr
from app.services.answer_intelligence import evaluate_structured_answer
from app.services.lesson_coaching import learning_profile, repair_plan
from app.services.assessment_insights import evidence_gate

router = APIRouter(prefix="/api/lesson", tags=["lesson"])

class StartLessonRequest(BaseModel):
    user_id: int
    lesson_id: int

@router.post("/start")
async def start_lesson(data: StartLessonRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    lesson = db.query(Lesson).filter(Lesson.id == data.lesson_id).first()
    if not user or not lesson:
        raise HTTPException(status_code=404, detail="User or lesson not found")
    session = LearningSession(id=str(uuid.uuid4()), user_id=user.id, lesson_id=lesson.id, status="active")
    db.add(session)
    db.commit()
    return {"session_id": session.id}

# Получить урок
@router.get("/{lesson_id}")
async def get_lesson(lesson_id: int, lang: str = "en", db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    public_content = localize_lesson_content(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level), lang)
    user = db.query(User).filter(User.telegram_id == authenticated_id).first()
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.topic == lesson.topic).first() if user else None
    recent_attempts = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id, ExerciseAttempt.lesson_id == lesson.id
    ).order_by(ExerciseAttempt.created_at.desc()).limit(4).all() if user else []
    profile = learning_profile(
        float(mastery.mastery or 0) if mastery else 0,
        [bool(item.correct) for item in reversed(recent_attempts)],
        int(mastery.correct_streak or 0) if mastery else 0,
    )
    audio_path = Path(__file__).resolve().parents[3] / "static" / "audio" / f"lesson_{lesson.id}.mp3"
    public_content["audio_url"] = f"/media/audio/lesson_{lesson.id}.mp3" if audio_path.exists() else None
    for exercise in public_content.get("exercises", []):
        exercise.pop("answer", None)
        exercise.pop("accepted_answers", None)
        exercise.pop("explanation", None)
        exercise.pop("model_answer", None)
        exercise.pop("target_patterns", None)
    return {
        "id": lesson.id,
        "level": lesson.level,
        "pillar": lesson.pillar,
        "topic": lesson.topic,
        "content": public_content,
        "xp_reward": lesson.xp_reward,
        "estimated_time": lesson.estimated_time,
        "learning_profile": profile,
    }

class CheckAnswerRequest(BaseModel):
    user_id: int
    lesson_id: int
    exercise_index: int
    answer: str
    confidence: str | None = None
    response_ms: int | None = None
    session_id: str
    language: str = "en"

def normalize_answer(value: str) -> str:
    value = re.sub(r"[.!?;,]+$", "", value.strip().lower())
    return re.sub(r"\s+", " ", value).replace("ß", "ss")

@router.post("/check-answer")
async def check_answer(data: CheckAnswerRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    lesson = db.query(Lesson).filter(Lesson.id == data.lesson_id).first()
    lesson_content = localize_lesson_content(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level), data.language) if lesson else {}
    exercises = lesson_content.get("exercises", [])
    if data.exercise_index < 0 or data.exercise_index >= len(exercises):
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise = exercises[data.exercise_index]
    accepted = exercise.get("accepted_answers") or [exercise.get("answer", "")]
    production_feedback = None
    structured_feedback = None
    if exercise.get("type") in {"production", "dialogue"}:
        production_feedback = await evaluate_production(data.answer, exercise, lesson_content, data.language)
        correct = production_feedback["correct"]
    else:
        structured_feedback = evaluate_structured_answer(data.answer, exercise)
        correct = structured_feedback["correct"]
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session = db.query(LearningSession).filter(LearningSession.id == data.session_id, LearningSession.user_id == user.id, LearningSession.lesson_id == lesson.id, LearningSession.status == "active").first()
    if not session:
        raise HTTPException(status_code=409, detail="Learning session is missing or closed")
    topic = lesson.topic
    db.add(ExerciseAttempt(
        user_id=user.id, lesson_id=lesson.id, session_id=session.id, exercise_index=data.exercise_index,
        topic=topic, answer=data.answer, correct=correct, confidence=data.confidence, response_ms=data.response_ms,
        production_score=(production_feedback or {}).get("score"),
        assessment={
            "dimensions": (production_feedback or {}).get("dimension_scores", {}),
            "cefr": (production_feedback or {}).get("cefr_standard"),
            "source": (production_feedback or {}).get("source"),
        } if production_feedback else None,
    ))
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.topic == topic).first()
    if not mastery:
        mastery = TopicMastery(user_id=user.id, topic=topic, mastery=0, attempts=0, correct_streak=0)
        db.add(mastery)
    mastery.attempts = (mastery.attempts or 0) + 1
    mastery.correct_streak = (mastery.correct_streak or 0) + 1 if correct else 0
    mastery.mastery = mastery_update_from_evidence(
        mastery.mastery or 0, production_feedback["score"], data.confidence, data.response_ms
    ) if production_feedback else mastery_update(mastery.mastery or 0, correct, data.confidence, data.response_ms)
    mastery.correct_total = (mastery.correct_total or 0) + (1 if correct else 0)
    mastery.lapse_count = (mastery.lapse_count or 0) + (0 if correct else 1)
    mastery.stability_days = next_stability(mastery.stability_days or 1, correct, data.confidence)
    mastery.last_answer_at = datetime.now()
    interval_days = review_interval(correct, mastery.correct_streak)
    mastery.next_review_at = datetime.now() + timedelta(days=interval_days)
    db.commit()
    skill = skill_for(topic)
    common_mistakes = lesson_content.get("common_mistakes") or []
    error_type = None if correct else ((production_feedback or {}).get("error_type") or (structured_feedback or {}).get("error_type") or exercise.get("misconception") or exercise.get("error_type") or skill.pillar)
    retry_copy = misconception_feedback(error_type, normalize_language(data.language)) if not correct else None
    missing_words = (production_feedback or {}).get("missing_words", []) if production_feedback else (structured_feedback or {}).get("missing_words", [])
    extra_words = (production_feedback or {}).get("extra_words", []) if production_feedback else (structured_feedback or {}).get("extra_words", [])
    return {
        "correct": correct,
        "correct_answer": production_feedback["corrected_answer"] if production_feedback else accepted[0],
        "explanation": production_feedback["feedback"] if production_feedback else exercise.get("explanation", ""),
        "production_score": production_feedback["score"] if production_feedback else None,
        "dimension_scores": production_feedback.get("dimension_scores") if production_feedback else None,
        "improvement": production_feedback.get("improvement") if production_feedback else None,
        "cefr_standard": production_feedback.get("cefr_standard") if production_feedback else None,
        "pass_mark": production_feedback.get("pass_mark") if production_feedback else None,
        "feedback_source": production_feedback["source"] if production_feedback else "rules",
        "mastery": round(mastery.mastery),
        "retention": retention_score(mastery.mastery, mastery.stability_days),
        "next_review_days": interval_days,
        "needs_support": not correct,
        "error_type": error_type,
        "contrast": common_mistakes[:2] if not correct else [],
        "retry_instruction": retry_copy,
        "production": exercise.get("type") in {"production", "dialogue"},
        "missing_words": missing_words,
        "extra_words": extra_words,
        "repair_steps": repair_plan(error_type, missing_words, extra_words, normalize_language(data.language)) if not correct else [],
        "next_action": "retry" if not correct else ("advance" if data.confidence == "sure" else "reinforce"),
    }

# Генерация упражнений (запасные)
class GenerateExercisesRequest(BaseModel):
    user_id: int
    lesson_id: int

@router.post("/generate-exercises")
async def generate_exercises(data: GenerateExercisesRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    raise HTTPException(status_code=410, detail="Use the validated lesson curriculum")

# Завершить урок (НОВЫЙ ЭНДПОИНТ)
class CompleteLessonRequest(BaseModel):
    user_id: int
    lesson_id: int
    session_id: str

@router.post("/complete")
async def complete_lesson(data: CompleteLessonRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    lesson = db.query(Lesson).filter(Lesson.id == data.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    session = db.query(LearningSession).filter(LearningSession.id == data.session_id, LearningSession.user_id == user.id, LearningSession.lesson_id == lesson.id, LearningSession.status == "active").first()
    if not session:
        raise HTTPException(status_code=409, detail="Learning session is missing or already completed")
    attempts = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id,
        ExerciseAttempt.lesson_id == data.lesson_id,
        ExerciseAttempt.session_id == session.id,
    ).all()
    summary = summarize_attempts(attempts)
    accuracy = summary["score"]
    passed = accuracy >= 70
    topic_mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.topic == lesson.topic).first()
    mastery_value = round(topic_mastery.mastery) if topic_mastery else 0
    session.score = accuracy
    session.status = "passed" if passed else "practice_needed"
    session.completed_at = datetime.now()

    # A lesson is completed only after demonstrated recall, not after opening every screen.
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user.id,
        UserProgress.lesson_id == data.lesson_id
    ).first()
    
    first_completion = passed and (not progress or not progress.completed)
    if not progress:
        progress = UserProgress(
            user_id=user.id,
            lesson_id=data.lesson_id,
            completed=passed,
            completed_at=datetime.now() if passed else None,
            score=accuracy
        )
        db.add(progress)
    else:
        progress.score = max(progress.score or 0, accuracy)
        if passed:
            progress.completed = True
            progress.completed_at = datetime.now()
    
    if first_completion:
        user.xp = (user.xp or 0) + lesson.xp_reward
        today = datetime.now().date()
        last_day = user.last_activity.date() if user.last_activity else None
        if last_day == today - timedelta(days=1):
            user.streak = (user.streak or 0) + 1
        elif last_day != today:
            user.streak = 1
        user.last_activity = datetime.now()
    checkpoint_ready = False
    lesson_track = (lesson.content or {}).get("track") if isinstance(lesson.content, dict) else None
    current_track = normalize_cefr(user.current_level)
    if passed and lesson_track == current_track:
        track_lessons = [item for item in db.query(Lesson).filter(Lesson.is_active == True).all() if isinstance(item.content, dict) and item.content.get("track") == current_track]
        track_ids = [item.id for item in track_lessons]
        completed_count = db.query(UserProgress).filter(UserProgress.user_id == user.id, UserProgress.lesson_id.in_(track_ids), UserProgress.completed == True).count() if track_ids else 0
        track_topics = {item.topic for item in track_lessons}
        mastery_values = [float(row.mastery or 0) for row in db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all() if row.topic in track_topics]
        completion_percent = round(completed_count / len(track_lessons) * 100) if track_lessons else 0
        average_mastery = round(sum(mastery_values) / len(mastery_values)) if mastery_values else 0
        production_attempts = db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == user.id, ExerciseAttempt.topic.in_(track_topics), ExerciseAttempt.assessment.isnot(None)).order_by(ExerciseAttempt.created_at.desc()).limit(100).all()
        checkpoint_ready = bool(next_cefr_track(current_track) and completion_percent >= 80 and average_mastery >= 70 and evidence_gate(production_attempts)["eligible"])
    db.commit()
    if passed:
        schedule_review(db, user.id, lesson.id)
    duration_seconds = max(0, round((session.completed_at.replace(tzinfo=None) - session.started_at.replace(tzinfo=None)).total_seconds())) if session.started_at else 0
    return {
        "status": "passed" if passed else "practice_needed",
        "passed": passed,
        "score": accuracy,
        "mastery": mastery_value,
        "xp_gained": lesson.xp_reward if first_completion else 0,
        "already_completed": bool(progress.completed and not first_completion),
        "streak": user.streak or 0,
        "first_try_correct": summary["first_try_correct"],
        "corrected_retries": summary["corrected_retries"],
        "needs_review": summary["needs_review"],
        "exercise_count": summary["exercise_count"],
        "duration_seconds": duration_seconds,
        "next_action": "plan" if passed else "retry",
        "checkpoint_ready": checkpoint_ready,
    }
