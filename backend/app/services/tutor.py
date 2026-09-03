# backend/app/services/tutor.py
import openai
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.user import User

openai.api_key = settings.OPENAI_API_KEY

def ask_tutor(db: Session, user_id: int, question: str) -> str:
    user = db.query(User).filter(User.id == user_id).first()
    level = user.current_level if user else 'A1'

    system_prompt = f"""
Ты — DeutschIQ Репетитор, эксперт по немецкому языку (уровень C2).
Отвечай всегда на русском языке. Уровень пользователя: {level}.

Правила:
- Для грамматики: дай правило (максимум 3 предложения), 3 примера, попроси пользователя составить свой пример.
- Для лексики: дай перевод, 2 контекста, предложение.
- Никогда не выдумывай слова. Если не уверен, скажи: "Я не уверен, давай проверим вместе".
- Будь доброжелательным и используй эмодзи.
"""
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

