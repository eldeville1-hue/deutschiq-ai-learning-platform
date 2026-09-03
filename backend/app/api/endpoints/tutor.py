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
from datetime import date

router = APIRouter(prefix="/api/tutor", tags=["tutor"])

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
    
    # 2. Если нет OpenAI ключа – вернуть заглушку
    if not client:
        return {
            "answer": "🔑 OpenAI API ключ не настроен. Добавьте OPENAI_API_KEY в .env."
        }
    
    # 3. Получить уровень и язык пользователя
    level = user.current_level or "A1"
    lang = user.language_code or "ru"
    diagnostic = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user.id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    weak_points = list((diagnostic.weak_points or {}).keys())[:4] if diagnostic else []
    
    # 4. Системный промпт
    system_prompt = f"""
You are DeutschIQ Tutor, a C2-level German teacher.
User level: {level}
Respond in: {lang}
Known weak areas: {', '.join(weak_points) if weak_points else 'not diagnosed yet'}

Rules:
- Explain grammar simply (max 3 sentences), give 2 examples
- For vocabulary: give translation + 2 example sentences
- Always correct mistakes politely
- If unsure, say "I'm not sure, let me check"
- Be encouraging and use emojis occasionally
- Keep answers under 200 words
- When relevant, connect the explanation to one known weak area, without repeating it in every answer
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
        db.add(TutorMessage(user_id=user.id, role="user", content=data.question))
        db.add(TutorMessage(user_id=user.id, role="assistant", content=answer))
        usage.questions_used += 1
        db.commit()
        return {"answer": answer, "remaining": max(0, daily_limit - usage.questions_used)}
        
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка AI: {str(e)}")

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
