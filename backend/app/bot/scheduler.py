# backend/app/bot/scheduler.py
import asyncio
from datetime import datetime, time, timedelta
from aiogram import Bot
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.progress import UserProgress

async def send_daily_reminders(bot: Bot):
    db = SessionLocal()
    sent = 0
    try:
        users = db.query(User).filter(
            User.last_activity < datetime.now() - timedelta(days=1)
        ).all()
        for user in users:
            try:
                lang = user.language_code if user.language_code in ("ru", "de", "en") else "en"
                text = {
                    "ru": "Твой короткий урок готов. Открой DeutschIQ, когда будет удобно.",
                    "de": "Deine kurze Lektion ist bereit. Öffne DeutschIQ, wenn es für dich passt.",
                    "en": "Your short lesson is ready. Open DeutschIQ when it suits you.",
                }[lang]
                await bot.send_message(
                    user.telegram_id,
                    text,
                )
                sent += 1
                await asyncio.sleep(0.1)
            except Exception:
                continue
    finally:
        db.close()
    print(f"📨 Отправлено {sent} напоминаний")
    return sent

async def schedule_daily_reminders(bot: Bot):
    while True:
        now = datetime.now()
        target = datetime.combine(now.date(), time(10, 0))
        if now > target:
            target += timedelta(days=1)
        wait_time = (target - now).total_seconds()
        print(f"⏳ Следующее напоминание через {wait_time/3600:.1f} часов")
        await asyncio.sleep(wait_time)
        await send_daily_reminders(bot)
