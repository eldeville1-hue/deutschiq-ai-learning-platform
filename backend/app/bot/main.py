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

def normalize_language(value: str | None) -> str:
    code = (value or "en").lower().split("-")[0]
    return code if code in ("ru", "de", "en") else "en"

def tr(lang: str, ru: str, de: str, en: str) -> str:
    return {"ru": ru, "de": de, "en": en}[normalize_language(lang)]

def build_web_app_url(user_id: int, route: str = "") -> str:
    parts = urlsplit(settings.WEBAPP_URL)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    path = route if route else parts.path
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), parts.fragment))

def main_keyboard(user_id: int, lang: str = "ru") -> ReplyKeyboardMarkup:
    open_text = tr(lang, "🇩🇪 Открыть DeutschIQ", "🇩🇪 DeutschIQ öffnen", "🇩🇪 Open DeutschIQ")
    progress_text = tr(lang, "📊 Мой прогресс", "📊 Mein Fortschritt", "📊 My progress")
    plan_text = tr(lang, "🗓 Мой план", "🗓 Mein Lernplan", "🗓 My plan")
    diagnostic_text = tr(lang, "📝 Диагностика", "📝 Diagnose", "📝 Placement test")
    help_text = tr(lang, "❓ Помощь", "❓ Hilfe", "❓ Help")
    placeholder = tr(lang, "Выберите действие", "Aktion auswählen", "Choose an action")
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
    return normalize_language(user.language_code if user else None)

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
        user = User(telegram_id=user_id, language_code=normalize_language(message.from_user.language_code))
        db.add(user)
        db.commit()
    lang = user_language(user)
    db.close()
    if (message.text or "").strip().lower().endswith(" subscribe"):
        await cmd_subscribe(message)
        return
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(
            text=tr(lang, "Открыть DeutschIQ", "DeutschIQ öffnen", "Open DeutschIQ"),
            web_app=WebAppInfo(url=build_web_app_url(user_id)),
        ),
    )
    start_text = tr(lang, "Добро пожаловать в DeutschIQ!\n\nОпредели уровень и начни персональный план.", "Willkommen bei DeutschIQ!\n\nBestimme dein Niveau und starte deinen persönlichen Lernplan.", "Welcome to DeutschIQ!\n\nFind your level and start your personal learning plan.")
    await message.answer(
        start_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=tr(lang, "Открыть DeutschIQ", "DeutschIQ öffnen", "Open DeutschIQ"), web_app=WebAppInfo(url=build_web_app_url(user_id)))]
        ])
    )
    await message.answer(tr(lang, "Меню:", "Menü:", "Menu:"), reply_markup=main_keyboard(user_id, lang))

@dp.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    db = SessionLocal()
    try:
        lang = user_language(db.query(User).filter(User.telegram_id == message.from_user.id).first())
    finally:
        db.close()
    if settings.BETA_FREE_ACCESS:
        await message.answer(
            tr(lang, "Во время тестирования все функции бесплатны.", "Während der Testphase sind alle Funktionen kostenlos.", "All features are free during testing.")
        )
        return
    prices = [LabeledPrice(label=tr(lang, "30 дней Pro", "30 Tage Pro", "30 days of Pro"), amount=700)]
    await message.answer_invoice(
        title="DeutschIQ Pro",
        description=tr(lang, "30 дней Pro", "30 Tage Pro", "30 days of Pro"),
        payload=f"sub_{message.from_user.id}_monthly",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="deutschiq_pro_30"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    lang = user_language(user)
    db.close()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=tr(lang, "Открыть DeutschIQ", "DeutschIQ öffnen", "Open DeutschIQ"),
            web_app=WebAppInfo(url=build_web_app_url(message.from_user.id)),
        )]
    ])
    help_text = tr(lang, "1. Пройди диагностику.\n2. Открой план.\n3. Выполняй один урок в день.\n4. Задавай вопросы репетитору.", "1. Starte die Diagnose.\n2. Öffne den Plan.\n3. Mache täglich eine Lektion.\n4. Frage den Tutor.", "1. Take the placement test.\n2. Open your plan.\n3. Complete one lesson a day.\n4. Ask the tutor.")
    await message.answer(
        help_text,
        reply_markup=keyboard,
    )

@dp.message(Command("profile"))
@dp.message(F.text == "📊 Мой прогресс")
@dp.message(F.text == "📊 Mein Fortschritt")
@dp.message(F.text == "📊 My progress")
async def cmd_profile(message: Message):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        if not user:
            await message.answer("Open DeutschIQ and take the placement test first.", reply_markup=main_keyboard(message.from_user.id, "en"))
            return
        lang = user_language(user)
        tariff = "Pro" if user.subscription_status == "pro" else tr(lang, "Бесплатно", "Kostenlos", "Free")
        text = tr(lang, f"Твой прогресс\n\nУровень: {user.current_level}\nXP: {user.xp or 0}\nСерия: {user.streak or 0}\nТариф: {tariff}", f"Dein Fortschritt\n\nNiveau: {user.current_level}\nXP: {user.xp or 0}\nSerie: {user.streak or 0}\nTarif: {tariff}", f"Your progress\n\nLevel: {user.current_level}\nXP: {user.xp or 0}\nStreak: {user.streak or 0}\nPlan: {tariff}")
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=tr(lang, "Открыть анализ", "Analyse öffnen", "Open analysis"),
                web_app=WebAppInfo(url=build_web_app_url(message.from_user.id, "/analytics")),
            )
        ]]))
    finally:
        db.close()

@dp.message(Command("plan"))
async def cmd_plan(message: Message):
    db = SessionLocal(); user = db.query(User).filter(User.telegram_id == message.from_user.id).first(); lang = user_language(user); db.close()
    await message.answer(tr(lang, "Твой учебный план:", "Dein Lernplan:", "Your learning plan:"), reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=tr(lang, "Открыть план", "Plan öffnen", "Open plan"), web_app=WebAppInfo(url=build_web_app_url(message.from_user.id, "/plan")))]
    ]))

@dp.message(F.text == "❓ Помощь")
@dp.message(F.text == "❓ Hilfe")
@dp.message(F.text == "❓ Help")
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
    lang = user_language(user)
    if user:
        user.subscription_status = "pro"
        user.subscription_end_date = datetime.now() + timedelta(days=30)
        db.commit()
    db.close()
    await message.answer(tr(lang, "Оплата прошла. Pro активирован.", "Zahlung erfolgreich. Pro ist aktiv.", "Payment successful. Pro is active."))

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
    if settings.BOT_MODE != "polling":
        raise RuntimeError("Standalone bot process is only for BOT_MODE=polling.")
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
        await bot.session.close()

if __name__ == "__main__":
    acquire_bot_lock(settings.BOT_TOKEN)
    asyncio.run(main())
