# backend/app/api/endpoints/plan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plan import generate_plan
from app.services.learning_route import CEFR_TRACKS, lesson_blockers, select_recommended_lesson, normalize_cefr, track_access
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

@router.get("/journey/{user_id}")
async def get_journey(user_id: int, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    lessons = db.query(Lesson).filter(Lesson.is_active == True).all()
    completed_ids = {row[0] for row in db.query(UserProgress.lesson_id).filter(UserProgress.user_id == user.id, UserProgress.completed == True).all()}
    mastery = {row.topic: float(row.mastery or 0) for row in db.query(TopicMastery).filter(TopicMastery.user_id == user.id).all()}
    result = []
    for level in (*CEFR_TRACKS, "C1"):
        track_lessons = [item for item in lessons if isinstance(item.content, dict) and item.content.get("track") == level]
        completed = sum(1 for item in track_lessons if item.id in completed_ids)
        mastered = [mastery[item.topic] for item in track_lessons if item.topic in mastery]
        average_mastery = round(sum(mastered) / len(mastered)) if mastered else 0
        completion = round(completed / len(track_lessons) * 100) if track_lessons else 0
        state = track_access(level, user.current_level)
        if state == "review" and completion >= 80 and average_mastery >= 70:
            state = "completed"
        result.append({"level": level, "state": state, "completion": completion, "mastery": average_mastery, "completed_lessons": completed, "total_lessons": len(track_lessons)})
    return {"current_level": normalize_cefr(user.current_level), "levels": result, "unlock_rule": {"completion": 80, "mastery": 70}}


@router.get("/{user_id}")
async def get_plan(user_id: int, lang: str | None = None, track: str | None = None, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    try:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            return {"error": f"Пользователь с telegram_id {user_id} не найден"}
        requested_track = normalize_cefr(track) if track else normalize_cefr(user.current_level)
        if track_access(requested_track, user.current_level) == "locked":
            raise HTTPException(status_code=403, detail="Complete your active level before opening this track")
        lessons = generate_plan(db, user.id, level=requested_track)
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
        a1_titles = {1: "Start & Orientierung", 2: "Sätze & Wörter", 3: "Alltagshandlungen", 4: "Im Alltag sprechen"}
        a2_titles = {1: "Fälle sicher nutzen", 2: "Über Vergangenes sprechen", 3: "Sätze verbinden", 4: "Selbstständig kommunizieren"}
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
            "week_title": ({"A1": a1_titles, "A2": a2_titles, "B1": b1_titles, "B2": b2_titles}.get((lesson.content or {}).get("track"), foundation_titles)).get((lesson.content or {}).get("week", min(index // 7 + 1, 4)), "Wiederholung"),
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
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        return []
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
