# backend/app/core/config.py
import os
import re
import logging
from dotenv import load_dotenv
from pathlib import Path

# Ищем .env сначала в backend, затем в корне проекта.
config_file = Path(__file__).resolve()
backend_dir = config_file.parents[2]
project_root = backend_dir.parent
possible_paths = [
    backend_dir / ".env",
    project_root / ".env",
]

env_path = None
for p in possible_paths:
    if p.exists():
        env_path = p
        break

if env_path:
    load_dotenv(dotenv_path=env_path)
    logging.getLogger("deutschiq.config").info("Loaded local environment file: %s", env_path)

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:5173")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    BOT_MODE = os.getenv("BOT_MODE", "polling").strip().lower()
    TELEGRAM_WEBHOOK_PATH = os.getenv("TELEGRAM_WEBHOOK_PATH", "/api/telegram/webhook").strip()
    TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "").strip()
    TASK_SECRET = os.getenv("TASK_SECRET", "").strip()

    def __init__(self):
        # Проверяем, что критические переменные загружены
        if not self.DATABASE_URL:
            raise ValueError("❌ DATABASE_URL не загружен! Проверьте .env файл.")
        if not self.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN не загружен! Проверьте .env файл.")
        if self.BOT_MODE not in {"polling", "webhook"}:
            raise ValueError("BOT_MODE must be either 'polling' or 'webhook'.")
        if not self.TELEGRAM_WEBHOOK_PATH.startswith("/api/"):
            raise ValueError("TELEGRAM_WEBHOOK_PATH must start with /api/.")
        if self.BOT_MODE == "webhook":
            if not self.WEBAPP_URL.startswith("https://"):
                raise ValueError("WEBAPP_URL must use HTTPS in webhook mode.")
            if not re.fullmatch(r"[A-Za-z0-9_-]{16,256}", self.TELEGRAM_WEBHOOK_SECRET):
                raise ValueError(
                    "TELEGRAM_WEBHOOK_SECRET must contain 16-256 letters, digits, '_' or '-'."
                )
            if len(self.TASK_SECRET) < 24:
                raise ValueError("TASK_SECRET must contain at least 24 characters in webhook mode.")

settings = Settings()
