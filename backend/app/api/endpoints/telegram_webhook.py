from aiogram.types import Update
from fastapi import APIRouter, Header, HTTPException, Request, status

from app.bot.main import bot, dp
from app.bot.scheduler import send_daily_reminders
from app.core.config import settings
from app.core.cloud_runtime import secret_matches


router = APIRouter(tags=["telegram"])


@router.post(settings.TELEGRAM_WEBHOOK_PATH, include_in_schema=False)
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if settings.BOT_MODE != "webhook":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not secret_matches(x_telegram_bot_api_secret_token, settings.TELEGRAM_WEBHOOK_SECRET):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid webhook secret")

    payload = await request.json()
    update = Update.model_validate(payload, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


@router.post("/api/tasks/daily-reminders", include_in_schema=False)
async def daily_reminders(x_task_secret: str | None = Header(default=None)):
    if not secret_matches(x_task_secret, settings.TASK_SECRET):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid task secret")
    sent = await send_daily_reminders(bot)
    return {"ok": True, "sent": sent}
