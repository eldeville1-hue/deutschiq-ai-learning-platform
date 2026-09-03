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
from app.services.learning_engine import mastery_update, review_interval, session_score
from app.services.content_quality import normalize_lesson_content
from app.services.production_feedback import evaluate_production

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
async def get_lesson(lesson_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    public_content = copy.deepcopy(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level))
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
        "estimated_time": lesson.estimated_time
    }

class CheckAnswerRequest(BaseModel):
    user_id: int
    lesson_id: int
    exercise_index: int
    answer: str
    confidence: str | None = None
    response_ms: int | None = None
    session_id: str

def normalize_answer(value: str) -> str:
    value = re.sub(r"[.!?;,]+$", "", value.strip().lower())
    return re.sub(r"\s+", " ", value).replace("ß", "ss")

@router.post("/check-answer")
async def check_answer(data: CheckAnswerRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    lesson = db.query(Lesson).filter(Lesson.id == data.lesson_id).first()
    lesson_content = normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level) if lesson else {}
    exercises = lesson_content.get("exercises", [])
    if data.exercise_index < 0 or data.exercise_index >= len(exercises):
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise = exercises[data.exercise_index]
    accepted = exercise.get("accepted_answers") or [exercise.get("answer", "")]
    production_feedback = None
    if exercise.get("type") == "production":
        production_feedback = await evaluate_production(data.answer, exercise, lesson_content)
        correct = production_feedback["correct"]
    else:
        correct = normalize_answer(data.answer) in {normalize_answer(str(item)) for item in accepted}
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session = db.query(LearningSession).filter(LearningSession.id == data.session_id, LearningSession.user_id == user.id, LearningSession.lesson_id == lesson.id, LearningSession.status == "active").first()
    if not session:
        raise HTTPException(status_code=409, detail="Learning session is missing or closed")
    topic = lesson.topic
    db.add(ExerciseAttempt(user_id=user.id, lesson_id=lesson.id, session_id=session.id, exercise_index=data.exercise_index, topic=topic, answer=data.answer, correct=correct, confidence=data.confidence, response_ms=data.response_ms))
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.topic == topic).first()
    if not mastery:
        mastery = TopicMastery(user_id=user.id, topic=topic, mastery=0, attempts=0, correct_streak=0)
        db.add(mastery)
    mastery.attempts = (mastery.attempts or 0) + 1
    mastery.correct_streak = (mastery.correct_streak or 0) + 1 if correct else 0
    mastery.mastery = mastery_update(mastery.mastery or 0, correct, data.confidence)
    interval_days = review_interval(correct, mastery.correct_streak)
    mastery.next_review_at = datetime.now() + timedelta(days=interval_days)
    db.commit()
    return {
        "correct": correct,
        "correct_answer": production_feedback["corrected_answer"] if production_feedback else accepted[0],
        "explanation": production_feedback["feedback"] if production_feedback else exercise.get("explanation", ""),
        "production_score": production_feedback["score"] if production_feedback else None,
        "feedback_source": production_feedback["source"] if production_feedback else "rules",
        "mastery": round(mastery.mastery),
        "next_review_days": interval_days,
        "needs_support": not correct,
        "production": exercise.get("type") == "production",
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
    accuracy = session_score([item.correct for item in attempts])
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
    db.commit()
    if passed:
        schedule_review(db, user.id, lesson.id)
    return {"status": "passed" if passed else "practice_needed", "passed": passed, "score": accuracy, "mastery": mastery_value, "xp_gained": lesson.xp_reward if first_completion else 0, "already_completed": bool(progress.completed and not first_completion), "streak": user.streak or 0}
