# backend/app/api/endpoints/tutor.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from openai import OpenAI, RateLimitError
import logging
from app.core.config import settings
from app.core.telegram_auth import telegram_user_id, assert_owner
from app.models.tutor import TutorMessage, TutorUsage
from app.models.event import ProductEvent
from app.models.learning import ExerciseAttempt, TopicMastery
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.services.plan import generate_plan
from app.services.tutor_context import build_tutor_learning_context, tutor_context_prompt
from app.services.tutor_fallback import fallback_answer
from datetime import date, datetime, timezone
from app.services.subscription import has_active_pro
from app.services.content_i18n import normalize_language

router = APIRouter(prefix="/api/tutor", tags=["tutor"])
logger = logging.getLogger(__name__)
# Avoid repeating requests when the provider explicitly reports exhausted credits.
_provider_quota_exhausted = False

def save_exchange(db: Session, user_id: int, question: str, answer: str, usage: "TutorUsage", daily_limit: int, mode: str, language: str):
    db.add(TutorMessage(user_id=user_id, role="user", content=question, language=language))
    db.add(TutorMessage(user_id=user_id, role="assistant", content=answer, language=language))
    usage.questions_used += 1
    db.add(ProductEvent(user_id=user_id, event_name="tutor_answered", properties={"mode": mode, "language": language}))
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
    language: str = "en"

@router.post("/ask")
async def ask_tutor(data: TutorRequest, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    global _provider_quota_exhausted
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
    daily_limit = settings.BETA_TUTOR_DAILY_LIMIT if settings.BETA_FREE_ACCESS else (999 if has_active_pro(user) else 3)
    if usage.questions_used >= daily_limit:
        raise HTTPException(status_code=429, detail="Daily tutor limit reached")
    
    # 2. Получить уровень и язык пользователя
    level = user.current_level or "A1"
    lang = normalize_language(data.language or user.language_code)
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user.id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    weak_points = list((diagnostic.weak_points or {}).keys())[:4] if diagnostic else []
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all()
    recent_attempts = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id,
    ).order_by(ExerciseAttempt.created_at.desc()).limit(100).all()
    plan = generate_plan(db, user.id, limit=30)
    completed_ids = {
        row[0] for row in db.query(UserProgress.lesson_id).filter(
            UserProgress.user_id == user.id,
            UserProgress.completed == True,
        ).all()
    }
    learner_context = build_tutor_learning_context(
        level=level,
        mastery_rows=mastery,
        recent_attempts=recent_attempts,
        plan=plan,
        completed_ids=completed_ids,
        weak_points=diagnostic.weak_points if diagnostic and diagnostic.weak_points else {},
        now=datetime.now(timezone.utc),
    )
    fallback_topics = (
        [item["topic"] for item in learner_context["recurring_errors"]]
        + learner_context["due_reviews"]
        + weak_points
        + [item["topic"] for item in learner_context["weak_skills"]]
    )

    # A provider outage or exhausted credit must not turn the tutor into a dead button.
    if not client or _provider_quota_exhausted:
        answer = fallback_answer(data.question, lang, level, fallback_topics)
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "local", lang)
    
    # 4. Системный промпт
    system_prompt = f"""
You are DeutschIQ Tutor, a C2-level German teacher.
User level: {level}
Respond only in: { {'ru': 'Russian', 'de': 'German', 'en': 'English'}[lang] }
Known diagnostic weak areas: {', '.join(weak_points) if weak_points else 'not diagnosed yet'}
{tutor_context_prompt(learner_context)}

Rules:
- Explain grammar simply (max 3 sentences), give 2 examples
- For vocabulary: give translation + 2 example sentences
- Always correct mistakes politely
- If unsure, say "I'm not sure, let me check"
- Be encouraging and use emojis occasionally
- Keep answers under 200 words
- When relevant, connect the explanation to one known weak area, without repeating it in every answer
- Never introduce grammar more than one CEFR step above the user's level
- Prioritize the current learning target, due retrieval, recurring errors, and production repair when relevant
- If the user asks about today's topic, use Current learning target; never infer it from the latest chat message
- If the user asks for practice, ask exactly one question, wait for the answer, then give corrective feedback
- During active practice, coach before revealing: give one small hint first. Do not provide the target answer unless the learner explicitly asks after trying or says they are stuck
- When correcting, identify the error category, show a minimal contrast, and ask for one fresh retry
- Treat recurring errors as misconceptions to repair, not as labels about the learner
- Do not pretend that a generated answer changes course mastery; only validated lesson/review attempts do
"""
    
    # 5. Собираем сообщения: системный промпт + история (если есть) + текущий вопрос
    messages = [{"role": "system", "content": system_prompt}]
    stored_history_query = db.query(TutorMessage).filter(TutorMessage.user_id == user.id, TutorMessage.language == lang)
    if diagnostic:
        stored_history_query = stored_history_query.filter(TutorMessage.created_at >= diagnostic.created_at)
    stored_history = stored_history_query.order_by(TutorMessage.created_at.desc()).limit(12).all()
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
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "ai", lang)
        
    except RateLimitError as exc:
        if "insufficient_quota" in str(exc) or "credit_balance_exhausted" in str(exc):
            _provider_quota_exhausted = True
            logger.warning("Tutor provider credits exhausted; switching to local tutor")
        else:
            logger.warning("Tutor provider rate limited; switching to local tutor")
        answer = fallback_answer(data.question, lang, level, fallback_topics)
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "local", lang)
    except Exception:
        logger.exception("Tutor provider unavailable; switching to local tutor")
        answer = fallback_answer(data.question, lang, level, fallback_topics)
        return save_exchange(db, user.id, data.question, answer, usage, daily_limit, "local", lang)

@router.get("/state/{user_id}")
async def tutor_state(user_id: int, lang: str = "en", db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    usage = db.query(TutorUsage).filter(TutorUsage.user_id == user.id, TutorUsage.usage_date == date.today()).first()
    pro = has_active_pro(user)
    limit = settings.BETA_TUTOR_DAILY_LIMIT if settings.BETA_FREE_ACCESS else (999 if pro else 3)
    language = normalize_language(lang)
    diagnostic = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
    history_query = db.query(TutorMessage).filter(TutorMessage.user_id == user.id, TutorMessage.language == language)
    if diagnostic:
        history_query = history_query.filter(TutorMessage.created_at >= diagnostic.created_at)
    history = history_query.order_by(TutorMessage.created_at.desc()).limit(30).all()
    return {"remaining": max(0, limit - (usage.questions_used if usage else 0)), "limit": limit, "is_pro": pro, "beta_free": settings.BETA_FREE_ACCESS, "messages": [{"role": item.role, "content": item.content} for item in reversed(history)]}
