# backend/app/services/exercise_generator.py
import openai
import json
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from app.models.lesson import Lesson

openai.api_key = settings.OPENAI_API_KEY

def generate_exercises(db: Session, user_id: int, lesson_id: int) -> list:
    """
    Генерирует персонализированные упражнения для пользователя на основе урока и его слабостей.
    Возвращает список упражнений в формате JSON.
    """
    # 1. Получаем пользователя и его слабости
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Пользователь не найден")
    
    # Берём последнюю диагностику
    diag = db.query(DiagnosticResult).filter(
        DiagnosticResult.user_id == user_id
    ).order_by(DiagnosticResult.created_at.desc()).first()
    
    weak_tags = list(diag.weak_points.keys()) if diag and diag.weak_points else []
    
    # 2. Получаем урок
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise ValueError("Урок не найден")
    
    # 3. Формируем промпт для OpenAI
    prompt = f"""
Ты — эксперт по немецкому языку. Создай 3 упражнения для ученика уровня {user.current_level} по теме "{lesson.topic}".

Слабые места ученика: {', '.join(weak_tags) if weak_tags else 'неизвестны'}.

Урок содержит следующее правило:
{lesson.content.get('rule', '')}

Примеры из урока:
{lesson.content.get('examples', [])}

Формат ответа — JSON-массив с объектами:
[
  {{
    "type": "fill",  // возможные типы: fill, choose, match, translate
    "question": "текст вопроса",
    "answer": "правильный ответ",
    "hint": "подсказка (опционально)"
  }}
]

Сделай упражнения разного типа и уровня сложности, соответствующие уровню ученика и его слабостям.
"""
    
    # 4. Запрашиваем OpenAI
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Ты — генератор упражнений по немецкому языку. Отвечай только JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    
    # 5. Парсим ответ
    try:
        exercises = json.loads(response.choices[0].message.content)
        return exercises
    except json.JSONDecodeError:
        # Запасной вариант, если JSON невалидный
        return [
            {"type": "fill", "question": "Вставьте пропущенное слово", "answer": "пример", "hint": "Подсказка"}
        ]

