# backend/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
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
    try:
        yield
    finally:
        await bot.session.close()


app = FastAPI(title="DeutschIQ API", version="14.0.0", lifespan=lifespan)

@app.get("/api/version")
async def version():
    return {"version": "14.0.0", "release": "cloud-webhook"}

@app.get("/api/health")
async def health():
    database = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database = "unavailable"
    return {
        "status": "ok" if database == "ok" else "degraded",
        "version": "14.0.0",
        "database": database,
        "bot_mode": settings.BOT_MODE,
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
    print(f"⚠️ Frontend not found at {frontend_path}. Run 'npm run build' first.")

@app.get("/")
async def root():
    if os.path.exists(frontend_path):
        response = FileResponse(os.path.join(frontend_path, "index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return {"status": "DeutschIQ API работает"}
