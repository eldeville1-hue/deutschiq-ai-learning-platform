# backend/init_db.py
import os
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv
from pathlib import Path
from app.models.base import Base
from app.models.user import User
from app.models.diagnostic import DiagnosticResult, DiagnosticMistake
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.payment import Payment
from app.models.tutor import TutorMessage, TutorUsage
from app.models.learning import ExerciseAttempt, TopicMastery, LearningSession

# Load a portable project-local environment file.
backend_dir = Path(__file__).resolve().parent
load_dotenv(backend_dir / ".env")
load_dotenv(backend_dir.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not found in .env file!")

engine = create_engine(DATABASE_URL)

# Створюємо всі таблиці
Base.metadata.create_all(bind=engine)

# Lightweight idempotent migration for existing installations.
columns = {column["name"] for column in inspect(engine).get_columns("users")}
if "diagnostic_completed" not in columns:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users ADD COLUMN diagnostic_completed BOOLEAN NOT NULL DEFAULT FALSE"))
        connection.execute(text("UPDATE users SET diagnostic_completed = TRUE WHERE id IN (SELECT DISTINCT user_id FROM diagnostic_results)"))

attempt_columns = {column["name"] for column in inspect(engine).get_columns("exercise_attempts")}
if "session_id" not in attempt_columns:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE exercise_attempts ADD COLUMN session_id VARCHAR(36) REFERENCES learning_sessions(id) ON DELETE CASCADE"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_exercise_attempts_session_id ON exercise_attempts (session_id)"))

print("✅ Таблицы созданы!")
