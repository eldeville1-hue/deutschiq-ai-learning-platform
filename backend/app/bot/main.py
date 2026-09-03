# backend/app/bot/main.py
import asyncio
import json
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery, Message, MenuButtonWebApp
from app.core.config import settings
from app.models.user import User
from app.core.database import SessionLocal
from app.bot.scheduler import schedule_daily_reminders
from app.core.single_instance import acquire_bot_lock

_start_cooldowns: dict[int, datetime] = {}

def build_web_app_url(user_id: int, route: str = "") -> str:
    parts = urlsplit(settings.WEBAPP_URL)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    path = route if route else parts.path
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), parts.fragment))

def main_keyboard(user_id: int, lang: str = "ru") -> ReplyKeyboardMarkup:
    if lang == "de":
        open_text, progress_text, plan_text, diagnostic_text, help_text, placeholder = (
            "🇩🇪 DeutschIQ öffnen", "📊 Mein Fortschritt", "🗓 Mein Lernplan",
            "📝 Diagnose", "❓ Hilfe", "Aktion auswählen",
        )
    else:
        open_text, progress_text, plan_text, diagnostic_text, help_text, placeholder = (
            "🇩🇪 Открыть DeutschIQ", "📊 Мой прогресс", "🗓 Мой план",
            "📝 Диагностика", "❓ Помощь", "Выберите действие",
        )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=open_text, web_app=WebAppInfo(url=build_web_app_url(user_id)))],
            [KeyboardButton(text=progress_text), KeyboardButton(text=plan_text, web_app=WebAppInfo(url=build_web_app_url(user_id, "/plan")))],
            [KeyboardButton(text=diagnostic_text, web_app=WebAppInfo(url=build_web_app_url(user_id, "/diagnostic"))), KeyboardButton(text=help_text)],
        ],
        resize_keyboard=True,
        input_field_placeholder=placeholder,
    )

def user_language(user: User | None) -> str:
    return user.language_code if user and user.language_code in ("ru", "de") else "ru"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# ХЕНДЛЕРЫ
# ==========================================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    now = datetime.now()
    last_sent = _start_cooldowns.get(user_id)
    if last_sent and now - last_sent < timedelta(seconds=8):
        logging.info("Ignored duplicate /start for user %s", user_id)
        return
    _start_cooldowns[user_id] = now
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        user = User(telegram_id=user_id)
        db.add(user)
        db.commit()
    lang = user_language(user)
    db.close()
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text="DeutschIQ öffnen" if lang == "de" else "Открыть DeutschIQ",
            web_app=WebAppInfo(url=build_web_app_url(user_id)),
        ),
    )
    start_text = (
        "Willkommen bei DeutschIQ!\n\nÖffne die App, bestimme dein Niveau "
        "und erhalte deinen persönlichen Lernplan."
        if lang == "de" else
        "Добро пожаловать в DeutschIQ!\n\nОткрой приложение, определи свой уровень "
        "и получи персональный план обучения."
    )
    await message.answer(
        start_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="DeutschIQ öffnen" if lang == "de" else "Открыть DeutschIQ", web_app=WebAppInfo(url=build_web_app_url(user_id)))]
        ])
    )
    await message.answer("Schnellmenü:" if lang == "de" else "Быстрое меню:", reply_markup=main_keyboard(user_id, lang))

@dp.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    prices = [LabeledPrice(label="1 месяц Pro-доступа", amount=700)]
    await message.answer_invoice(
        title="DeutschIQ Pro",
        description="Полный доступ к диагностике, плану, ИИ-репетитору и всем урокам",
        payload=f"sub_{message.from_user.id}_monthly",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="deutschiq_sub"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    lang = user_language(user)
    db.close()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="DeutschIQ öffnen" if lang == "de" else "Открыть DeutschIQ",
            web_app=WebAppInfo(url=build_web_app_url(message.from_user.id)),
        )]
    ])
    help_text = (
        "So verwendest du DeutschIQ\n\n1. Starte die Diagnose.\n"
        "2. Öffne deinen persönlichen Lernplan.\n3. Mache täglich eine kurze Lektion.\n"
        "4. Stelle dem KI-Tutor deine Fragen.\n\n"
        "Befehle:\n/start — App öffnen\n/help — Hilfe\n/subscribe — Pro aktivieren"
        if lang == "de" else
        "Как пользоваться DeutschIQ\n\n1. Пройди диагностику уровня.\n"
        "2. Открой персональный план.\n3. Выполняй один короткий урок ежедневно.\n"
        "4. Задавай вопросы ИИ-репетитору.\n\n"
        "Команды:\n/start — открыть приложение\n/help — помощь\n/subscribe — оформить Pro"
    )
    await message.answer(
        help_text,
        reply_markup=keyboard,
    )

@dp.message(Command("profile"))
@dp.message(F.text == "📊 Мой прогресс")
@dp.message(F.text == "📊 Mein Fortschritt")
async def cmd_profile(message: Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        if not user:
            await message.answer("Сначала пройди диагностику в DeutschIQ.", reply_markup=main_keyboard(message.from_user.id))
            return
        lang = user_language(user)
        tariff = ("Pro" if user.subscription_status == "pro" else ("Kostenlos" if lang == "de" else "Бесплатный"))
        text = (
            f"Dein Fortschritt\n\nNiveau: {user.current_level}\nXP: {user.xp or 0}\n"
            f"Serie: {user.streak or 0} Tage\nTarif: {tariff}"
            if lang == "de" else
            f"Твой прогресс\n\nУровень: {user.current_level}\nОпыт: {user.xp or 0} XP\n"
            f"Серия: {user.streak or 0} дней\nТариф: {tariff}"
        )
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="Analyse öffnen" if lang == "de" else "Открыть подробный анализ",
                web_app=WebAppInfo(url=build_web_app_url(message.from_user.id, "/analytics")),
            )
        ]]))
    finally:
        db.close()

@dp.message(Command("plan"))
async def cmd_plan(message: Message):
    await message.answer("🗓 Твой персональный 30-дневный план:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть план", web_app=WebAppInfo(url=build_web_app_url(message.from_user.id, "/plan")))]
    ]))

@dp.message(F.text == "❓ Помощь")
@dp.message(F.text == "❓ Hilfe")
async def help_button(message: Message):
    await cmd_help(message)

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(lambda m: m.successful_payment is not None)
async def successful_payment(message: Message):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if user:
        user.subscription_status = "pro"
        user.subscription_end_date = datetime.now() + timedelta(days=30)
        db.commit()
    db.close()
    await message.answer(
        "✅ Оплата успешна! Ваш Pro-план активен.\n"
        "Возвращайтесь в Mini App, чтобы начать уроки."
    )

@dp.message(lambda m: m.web_app_data is not None)
async def handle_web_app_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except (TypeError, json.JSONDecodeError):
        logging.warning("Invalid web_app_data from user %s", message.from_user.id)
        return
    if data.get('command') == '/subscribe':
        await cmd_subscribe(message)

# ==========================================
# ЗАПУСК
# ==========================================

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="OPEN DeutschIQ",
            web_app=WebAppInfo(url=settings.WEBAPP_URL),
        )
    )
    reminder_task = asyncio.create_task(schedule_daily_reminders(bot))
    print("🚀 Бот запущен и готов принимать команды")
    try:
        await dp.start_polling(bot)
    finally:
        reminder_task.cancel()

if __name__ == "__main__":
    acquire_bot_lock(settings.BOT_TOKEN)
    asyncio.run(main())
