# backend/app/core/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Ищем .env – сначала в папке backend, потом на уровень выше (корень)
possible_paths = [
    Path(__file__).resolve().parent.parent / ".env",      # backend/.env
    Path(__file__).resolve().parent.parent.parent / ".env",  # корень проекта
]

env_path = None
for p in possible_paths:
    if p.exists():
        env_path = p
        break

if env_path:
    load_dotenv(dotenv_path=env_path)
    print(f"✅ .env загружен из {env_path}")
else:
    print("⚠️ .env не найден! Проверьте, что файл существует.")

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:5173")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    def __init__(self):
        # Проверяем, что критические переменные загружены
        if not self.DATABASE_URL:
            raise ValueError("❌ DATABASE_URL не загружен! Проверьте .env файл.")
        if not self.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN не загружен! Проверьте .env файл.")

settings = Settings()
