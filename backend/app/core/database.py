# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine_options = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
if settings.DATABASE_URL.startswith("postgresql"):
    # Не заставляем Mini App ждать десятки секунд, если PostgreSQL выключен.
    engine_options["connect_args"] = {"connect_timeout": 2}

engine = create_engine(settings.DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
