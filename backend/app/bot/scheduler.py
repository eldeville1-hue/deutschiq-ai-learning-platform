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
    today = datetime.now().date()
    
    users = db.query(User).filter(
        User.last_activity < datetime.now() - timedelta(days=1)
    ).all()
    
    sent = 0
    for user in users:
        try:
            await bot.send_message(
                user.telegram_id,
                "🇩🇪 Доброе утро! 🌅\n\n"
                "Не забудь пройти сегодняшний урок в DeutschIQ!\n"
                "Каждый день приближает тебя к цели 🎯\n\n"
                "👉 Открой бота и нажми 'Открыть DeutschIQ'"
            )
            sent += 1
            await asyncio.sleep(0.1)
        except:
            pass
    
    db.close()
    print(f"📨 Отправлено {sent} напоминаний")

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

