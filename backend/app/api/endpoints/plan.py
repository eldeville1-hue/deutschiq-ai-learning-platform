# backend/app/api/endpoints/plan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plan import generate_plan
from app.services.learning_route import lesson_blockers, select_recommended_lesson
from app.models.user import User
from app.models.diagnostic import DiagnosticResult
from app.models.progress import UserProgress
from app.models.learning import TopicMastery
import traceback
from sqlalchemy.exc import SQLAlchemyError
from app.core.telegram_auth import telegram_user_id, assert_owner
from datetime import datetime, timezone
from app.services.content_i18n import localize_lesson_content
from app.services.content_i18n import normalize_language
from app.services.content_quality import normalize_lesson_content

router = APIRouter(prefix="/api/plan", tags=["plan"])

@router.get("/{user_id}")
async def get_plan(user_id: int, lang: str | None = None, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            return {"error": f"Пользователь с telegram_id {user_id} не найден"}
        lessons = generate_plan(db, user.id)
        completed_ids = {
            row[0] for row in db.query(UserProgress.lesson_id).filter(
                UserProgress.user_id == user.id,
                UserProgress.completed == True,
            ).all()
        }
        mastery_rows = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all()
        mastery = {row.topic: round(row.mastery) for row in mastery_rows}
        diagnostic = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
        weak_points = diagnostic.weak_points if diagnostic and diagnostic.weak_points else {}
        recommended = select_recommended_lesson(lessons, completed_ids, mastery, weak_points)
        foundation_titles = {
            1: "Satzbau",
            2: "Dativ & Akkusativ",
            3: "Der, Die, Das",
            4: "Perfekt",
        }
        b1_titles = {
            1: "Satzverknüpfung",
            2: "Passiv & Modalität",
            3: "Grammatische Präzision",
            4: "Schreiben & Sprechen",
        }
        b2_titles = {
            1: "Verknüpfen & Verdichten",
            2: "Formeller Ausdruck",
            3: "Argumentieren & Schreiben",
            4: "Diskutieren & Präsentieren",
        }
        language = normalize_language(lang or user.language_code)
        return [{
            "id": lesson.id,
            "day": (lesson.content or {}).get("day", index + 1),
            "week": (lesson.content or {}).get("week", min(index // 7 + 1, 4)),
            "week_title": ({"B1": b1_titles, "B2": b2_titles}.get((lesson.content or {}).get("track"), foundation_titles)).get((lesson.content or {}).get("week", min(index // 7 + 1, 4)), "Wiederholung"),
            "track": (lesson.content or {}).get("track", "foundation"),
            "topic": lesson.topic,
            "title": localize_lesson_content(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level), language).get("title", lesson.topic),
            "pillar": lesson.pillar,
            "level": lesson.level,
            "estimated_time": lesson.estimated_time,
            "completed": lesson.id in completed_ids,
            "mastery": mastery.get(lesson.topic),
            "blocked_by": lesson_blockers(lesson, lessons, completed_ids, mastery),
            "recommended": bool(recommended and lesson.id == recommended.id),
            "recommendation_reason": (
                "review_due" if any(row.topic == lesson.topic and row.next_review_at and (row.next_review_at if row.next_review_at.tzinfo else row.next_review_at.replace(tzinfo=timezone.utc)) <= datetime.now(timezone.utc) for row in mastery_rows)
                else "build_foundation" if mastery.get(lesson.topic) is None
                else "improve_mastery"
            ),
        } for index, lesson in enumerate(lessons)]
    except SQLAlchemyError:
        db.rollback()
        return []
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
