from datetime import date
from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.learning import LearningSession, SpeechAttempt, SpeechUsage
from app.models.lesson import Lesson
from app.models.user import User
from app.services.content_quality import normalize_lesson_content
from app.services.speech_assessment import assess_speech_match

router = APIRouter(prefix="/api/speech", tags=["speech"])
ALLOWED_AUDIO_TYPES = {"audio/webm", "audio/mp4", "audio/mpeg", "audio/wav", "audio/ogg"}


async def read_audio(audio: UploadFile) -> tuple[bytes, str]:
    media_type = (audio.content_type or "").split(";", 1)[0].lower()
    if media_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported audio format")
    payload = await audio.read(settings.SPEECH_MAX_BYTES + 1)
    if not payload or len(payload) > settings.SPEECH_MAX_BYTES:
        raise HTTPException(status_code=413, detail="Audio must be between 1 byte and 5 MB")
    return payload, media_type


def reserve_usage(db: Session, user: User, payload_size: int) -> SpeechUsage:
    today = date.today().isoformat()
    usage = db.query(SpeechUsage).filter(SpeechUsage.user_id == user.id, SpeechUsage.usage_date == today).first()
    if not usage:
        usage = SpeechUsage(user_id=user.id, usage_date=today)
        db.add(usage)
    if usage.requests_used >= settings.SPEECH_DAILY_LIMIT:
        raise HTTPException(status_code=429, detail="Daily speech practice limit reached")
    usage.requests_used += 1
    usage.audio_bytes += payload_size
    return usage


async def openai_transcript(payload: bytes, media_type: str, filename: str, prompt: str) -> str:
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="Speech recognition is temporarily unavailable")
    try:
        result = await AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=20).audio.transcriptions.create(
            model=settings.OPENAI_TRANSCRIBE_MODEL,
            file=(filename, BytesIO(payload), media_type),
            language="de",
            prompt=prompt[:200] or "German language practice",
        )
        return (result.text or "").strip()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Speech recognition is temporarily unavailable") from exc


@router.post("/transcribe")
async def transcribe_speech(
    user_id: int = Form(...),
    lesson_id: int = Form(...),
    exercise_index: int = Form(...),
    session_id: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    authenticated_id: int = Depends(telegram_user_id),
):
    assert_owner(authenticated_id, user_id)
    payload, media_type = await read_audio(audio)

    user = db.query(User).filter(User.telegram_id == user_id).first()
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not user or not lesson:
        raise HTTPException(status_code=404, detail="User or lesson not found")
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == user.id,
        LearningSession.lesson_id == lesson.id,
        LearningSession.status == "active",
    ).first()
    if not session:
        raise HTTPException(status_code=409, detail="Learning session is missing or closed")

    content = normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level)
    exercises = content.get("exercises", [])
    if exercise_index < 0 or exercise_index >= len(exercises):
        raise HTTPException(status_code=404, detail="Exercise not found")
    exercise = exercises[exercise_index]
    target = str((exercise.get("accepted_answers") or [exercise.get("answer", "")])[0])
    filename = audio.filename or "speech.webm"
    transcript = await openai_transcript(payload, media_type, filename, target)
    usage = reserve_usage(db, user, len(payload))
    match = assess_speech_match(transcript, target) if target else None
    modality = "listening" if exercise.get("type") == "listening" else "speaking"
    db.add(SpeechAttempt(user_id=user.id, lesson_id=lesson.id, modality=modality,
                         match_score=match["score"] if match else None,
                         recognized_words=len(transcript.split())))
    db.commit()
    return {
        "transcript": transcript,
        "match": match,
        "remaining": max(settings.SPEECH_DAILY_LIMIT - usage.requests_used, 0),
        "assessment_scope": "recognized_words_not_accent",
    }


@router.post("/tutor-transcribe")
async def transcribe_tutor_message(
    user_id: int = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    authenticated_id: int = Depends(telegram_user_id),
):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    payload, media_type = await read_audio(audio)
    transcript = await openai_transcript(payload, media_type, audio.filename or "speech.webm", "German learner speaking to a tutor")
    usage = reserve_usage(db, user, len(payload))
    db.commit()
    return {"transcript": transcript, "remaining": max(settings.SPEECH_DAILY_LIMIT - usage.requests_used, 0)}


@router.get("/progress/{user_id}")
async def speech_progress(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    rows = db.query(SpeechAttempt).filter(SpeechAttempt.user_id == user.id).all()
    result = {}
    for modality in ("speaking", "listening"):
        items = [row for row in rows if row.modality == modality]
        scored = [row.match_score for row in items if row.match_score is not None]
        result[modality] = {
            "attempts": len(items),
            "score": round(sum(scored) / len(scored)) if scored else None,
            "status": "assessed" if scored else "not_assessed",
        }
    return result
