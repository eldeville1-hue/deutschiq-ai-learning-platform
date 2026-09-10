# backend/app/api/endpoints/tutor.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from openai import OpenAI
from app.core.config import settings
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.models.tutor import TutorMessage, TutorUsage
from app.models.learning import ExerciseAttempt, TopicMastery
from app.models.lesson import Lesson
from app.services.tutor_fallback import fallback_answer
from datetime import date

router = APIRouter(prefix="/api/tutor", tags=["tutor"])

def save_exchange(db: Session, user_id: int, question: str, answer: str, usage: "TutorUsage", daily_limit: int, mode: str):
    db.add(TutorMessage(user_id=user_id, role="user", content=question))
    db.add(TutorMessage(user_id=user_id, role="assistant", content=answer))
    usage.questions_used += 1
    db.commit()
    return {"answer": answer, "remaining": max(0, daily_limit - usage.questions_used), "mode": mode}

# Инициализация OpenAI
client = None
if settings.OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        print("✅ OpenAI client initialized")
    except Exception as e:
        print(f"❌ OpenAI init error: {e}")

class TutorRequest(BaseModel):
    user_id: int
    question: str
    history: Optional[List[dict]] = None   # <-- НОВОЕ ПОЛЕ

@router.post("/ask")
async def ask_tutor(data: TutorRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, data.user_id)
    # 1. Найти пользователя
    user = db.query(User).filter(User.telegram_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    today = date.today()
    usage = db.query(TutorUsage).filter(TutorUsage.user_id == user.id, TutorUsage.usage_date == today).first()
    if not usage:
        usage = TutorUsage(user_id=user.id, usage_date=today, questions_used=0)
        db.add(usage)
        db.flush()
    daily_limit = 999 if user.subscription_status == "pro" else 3
    if usage.questions_used >= daily_limit:
        raise HTTPException(status_code=429, detail="Daily tutor limit reached")
    
    # 2. Получить уровень и язык пользователя
    level = user.current_level or "A1"
    lang = user.language_code or "ru"
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user.id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    weak_points = list((diagnostic.weak_points or {}).keys())[:4] if diagnostic else []
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).order_by(TopicMastery.mastery.asc()).limit(5).all()
    recent_errors = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id,
        ExerciseAttempt.correct == False,
    ).order_by(ExerciseAttempt.created_at.desc()).limit(4).all()
    latest_lesson_id = recent_errors[0].lesson_id if recent_errors else None
    latest_lesson = db.query(Lesson).filter(Lesson.id == latest_lesson_id).first() if latest_lesson_id else None
    mastery_context = ", ".join(f"{item.topic}: {round(item.mastery)}%" for item in mastery) or "no practice data"
    error_context = ", ".join(item.topic for item in recent_errors) or "no recent errors"
    fallback_topics = [item.topic for item in recent_errors] + weak_points + [item.topic for item in mastery]

    # A provider outage or exhausted credit must not turn the tutor into a dead button.
    if not client:
        answer = fallback_answer(data.question, lang, level, fallback_topics)
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "local")
    
    # 4. Системный промпт
    system_prompt = f"""
You are DeutschIQ Tutor, a C2-level German teacher.
User level: {level}
Respond in: {lang}
Known weak areas: {', '.join(weak_points) if weak_points else 'not diagnosed yet'}
Current mastery: {mastery_context}
Recent error topics: {error_context}
Current lesson: {latest_lesson.topic if latest_lesson else 'not started'}

Rules:
- Explain grammar simply (max 3 sentences), give 2 examples
- For vocabulary: give translation + 2 example sentences
- Always correct mistakes politely
- If unsure, say "I'm not sure, let me check"
- Be encouraging and use emojis occasionally
- Keep answers under 200 words
- When relevant, connect the explanation to one known weak area, without repeating it in every answer
- Never introduce grammar more than one CEFR step above the user's level
- If the user asks for practice, ask exactly one question, wait for the answer, then give corrective feedback
- When correcting, identify the error category, show a minimal contrast, and ask for one fresh retry
- Do not pretend that a generated answer changes course mastery; only validated lesson attempts do
"""
    
    # 5. Собираем сообщения: системный промпт + история (если есть) + текущий вопрос
    messages = [{"role": "system", "content": system_prompt}]
    stored_history = db.query(TutorMessage).filter(TutorMessage.user_id == user.id).order_by(TutorMessage.created_at.desc()).limit(12).all()
    messages.extend({"role": item.role, "content": item.content} for item in reversed(stored_history))
    messages.append({"role": "user", "content": data.question})
    
    # 6. Запрос к OpenAI
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL or "gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        answer = response.choices[0].message.content
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "ai")
        
    except Exception as e:
        print(f"❌ OpenAI error, using local tutor: {e}")
        answer = fallback_answer(data.question, lang, level, fallback_topics)
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "local")

@router.get("/state/{user_id}")
async def tutor_state(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    usage = db.query(TutorUsage).filter(TutorUsage.user_id == user.id, TutorUsage.usage_date == date.today()).first()
    limit = 999 if user.subscription_status == "pro" else 3
    history = db.query(TutorMessage).filter(TutorMessage.user_id == user.id).order_by(TutorMessage.created_at.desc()).limit(30).all()
    return {"remaining": max(0, limit - (usage.questions_used if usage else 0)), "messages": [{"role": item.role, "content": item.content} for item in reversed(history)]}
