# backend/app/main.py
from contextlib import asynccontextmanager
import logging
import time
import uuid
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import diagnostic, dashboard, plan, tutor, lesson, badges, mistakes, stats, referral, user_state, learning, telegram_webhook
import os
from app.core.config import settings
from app.core.database import engine
from sqlalchemy import text
from aiogram.types import MenuButtonWebApp, WebAppInfo
from app.bot.main import bot
from app.core.cloud_runtime import public_origin
from app.core.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("deutschiq.api")
VERSION = "15.0.0"

@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.BOT_MODE == "webhook":
        base_url = settings.WEBAPP_URL.rstrip("/")
        await bot.set_webhook(
            url=f"{base_url}{settings.TELEGRAM_WEBHOOK_PATH}",
            secret_token=settings.TELEGRAM_WEBHOOK_SECRET,
            drop_pending_updates=False,
        )
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="OPEN DeutschIQ",
                web_app=WebAppInfo(url=settings.WEBAPP_URL),
            )
        )
        logger.info("Telegram webhook configured")
    try:
        yield
    finally:
        await bot.session.close()


app = FastAPI(title="DeutschIQ API", version=VERSION, lifespan=lifespan)

@app.middleware("http")
async def request_logging(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request error", extra={"request_id": request_id, "method": request.method, "path": request.url.path})
        raise
    response.headers["X-Request-ID"] = request_id
    logger.info("Request completed", extra={"request_id": request_id, "method": request.method, "path": request.url.path, "status_code": response.status_code, "duration_ms": round((time.perf_counter() - started) * 1000, 2)})
    return response

@app.get("/api/version")
async def version():
    return {"version": VERSION, "release": "production-hardening"}

@app.get("/api/health/live")
async def liveness():
    return {"status": "ok", "version": VERSION}

@app.get("/api/health")
async def health():
    database = "ok"
    migrations = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database = "unavailable"
        migrations = "unknown"
    if database == "ok":
        try:
            with engine.connect() as connection:
                revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one_or_none()
                migrations = revision or "missing"
        except Exception:
            migrations = "missing"
    return {
        "status": "ok" if database == "ok" and migrations != "missing" else "degraded",
        "version": VERSION,
        "database": database,
        "migrations": migrations,
        "bot_mode": settings.BOT_MODE,
        "webhook_configured": settings.BOT_MODE == "webhook" and bool(settings.TELEGRAM_WEBHOOK_SECRET),
        "ai_feedback": "configured" if bool(settings.OPENAI_API_KEY) else "fallback",
    }

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[public_origin(settings.WEBAPP_URL)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostic.router)
app.include_router(dashboard.router)
app.include_router(plan.router)
app.include_router(tutor.router)
app.include_router(lesson.router)
app.include_router(badges.router)
app.include_router(mistakes.router)
app.include_router(stats.router)
app.include_router(referral.router)
app.include_router(user_state.router)
app.include_router(learning.router)
app.include_router(telegram_webhook.router)

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/mini-app/dist")

if os.path.exists(frontend_path):
    assets_path = os.path.join(frontend_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "API endpoint not found"}
        file_path = os.path.join(frontend_path, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            response = FileResponse(file_path)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
        response = FileResponse(os.path.join(frontend_path, "index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
else:
    logger.warning("Frontend build not found at %s", frontend_path)

@app.get("/")
async def root():
    if os.path.exists(frontend_path):
        response = FileResponse(os.path.join(frontend_path, "index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return {"status": "DeutschIQ API работает"}
