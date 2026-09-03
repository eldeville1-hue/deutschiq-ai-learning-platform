# backend/generate_audio.py
import os
from pathlib import Path
from gtts import gTTS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.lesson import Lesson

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
db = Session()

# Папка для аудиофайлов
AUDIO_DIR = Path(__file__).parent / "static/audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Находим уроки с пилларом listening или pronunciation
lessons = db.query(Lesson).filter(
    Lesson.pillar.in_(["listening", "pronunciation"])
).all()

print(f"🔊 Генерация аудио для {len(lessons)} уроков...")

for lesson in lessons:
    # Берём первое предложение из примеров или правила
    text = lesson.content.get("examples", [""])[0]
    if not text:
        text = lesson.content.get("rule", "")

    # Создаём имя файла
    filename = f"lesson_{lesson.id}.mp3"
    filepath = AUDIO_DIR / filename

    # Генерируем аудио
    try:
        tts = gTTS(text=text, lang='de')
        tts.save(str(filepath))
        print(f"✅ {lesson.topic}: {filename}")
    except Exception as e:
        print(f"❌ Ошибка для {lesson.topic}: {e}")

print("🎵 Готово!")

