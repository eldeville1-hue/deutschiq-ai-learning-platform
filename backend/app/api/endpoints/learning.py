from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.telegram_auth import assert_owner, telegram_user_id
from app.models.learning import TopicMastery
from app.models.learning import ExerciseAttempt
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.diagnostic import DiagnosticResult
from app.models.user import User
from app.services.learning_engine import adaptive_priority_score, retention_score
from app.services.lesson_coaching import repeated_error_focus
from app.services.plan import generate_plan
from app.services.learning_route import lesson_blockers, select_recommended_lesson
from app.services.skill_graph import skill_for
from app.services.content_quality import normalize_lesson_content
from app.services.content_i18n import localize_lesson_content, normalize_language
from app.services.assessment_insights import assessment_insights

router = APIRouter(prefix="/api/learning", tags=["learning"])


def _days_overdue(review_at, now: datetime) -> float:
    if not review_at:
        return 0.0
    if review_at.tzinfo is None:
        review_at = review_at.replace(tzinfo=timezone.utc)
    return max(0.0, (now - review_at).total_seconds() / 86_400)


@router.get("/today/{user_id}")
async def today(user_id: int, lang: str | None = None, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    due = db.query(TopicMastery).filter(
        TopicMastery.user_id == user.id,
        TopicMastery.next_review_at.isnot(None),
        TopicMastery.next_review_at <= now,
    ).order_by(TopicMastery.mastery.asc()).all()
    mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id).order_by(TopicMastery.mastery.asc()).all()
    mastery_map = {item.topic: item.mastery for item in mastery}
    retention_map = {
        item.topic: adaptive_priority_score(
            item.mastery,
            item.stability_days or 1,
            _days_overdue(item.next_review_at, now),
        )
        for item in mastery
    }
    plan = generate_plan(db, user.id, limit=30)
    completed_ids = {
        row[0] for row in db.query(UserProgress.lesson_id).filter(
            UserProgress.user_id == user.id,
            UserProgress.completed == True,
        ).all()
    }
    diagnostic = db.query(DiagnosticResult).filter(DiagnosticResult.user_id == user.id).order_by(DiagnosticResult.created_at.desc()).first()
    weak_points = diagnostic.weak_points if diagnostic and diagnostic.weak_points else {}
    recent_skill_rows = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id,
    ).order_by(ExerciseAttempt.created_at.desc(), ExerciseAttempt.id.desc()).limit(12).all()
    focus_skill = repeated_error_focus(
        [{"skill_id": item.topic, "correct": bool(item.correct)}
         for item in reversed(recent_skill_rows)],
        {lesson.topic for lesson in plan},
    )
    next_lesson = select_recommended_lesson(
        plan, completed_ids, mastery_map, weak_points, retention_map, focus_skill=focus_skill,
    )
    production_attempts = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user.id, ExerciseAttempt.assessment.isnot(None)
    ).order_by(ExerciseAttempt.created_at.desc()).limit(100).all()
    assessment = assessment_insights(production_attempts)
    repair_focus = assessment["priority_topics"][0] if assessment["priority_topics"] else None
    language = normalize_language(lang or user.language_code)
    next_content = localize_lesson_content(normalize_lesson_content(next_lesson.content or {}, next_lesson.topic, next_lesson.level), language) if next_lesson else {}
    due_count = len(due)
    # A daily session stays short enough to finish: at most two retrievals,
    # one compact teaching block, and one independent mission.
    review_count = min(2, due_count)
    phases = []
    if review_count:
        phases.append({"kind": "review", "count": review_count, "minutes": 2 if review_count == 1 else 3, "reason": "due"})
    if next_lesson:
        weakest = mastery[0] if mastery else None
        if not review_count and repair_focus and repair_focus["score"] < 70:
            repair_lesson = next((item for item in plan if item.topic == repair_focus["topic"]), None)
            phases.append({"kind": "repair", "count": 1, "minutes": 2, "topic": repair_focus["topic"], "dimension": repair_focus["dimension"], "score": repair_focus["score"], "lesson_id": repair_lesson.id if repair_lesson else None, "reason": "weak_assessment_dimension"})
        elif not review_count and weakest and weakest.mastery < 70 and weakest.topic not in {item.topic for item in due[:2]}:
            phases.append({"kind": "repair", "count": 1, "minutes": 2, "topic": weakest.topic, "reason": "weak_mastery"})
        phases.append({
            "kind": "learn",
            "count": 1,
            "minutes": 4,
            "lesson_id": next_lesson.id,
            "topic": next_lesson.topic,
            "title": next_content.get("title", next_lesson.topic),
            "reason": "weakest_ready_skill" if mastery else "first_step",
            "prerequisites": list(skill_for(next_lesson.topic).prerequisites),
        })
        phases.append({"kind": "mission", "count": 1, "minutes": 2, "topic": next_lesson.topic, "reason": "independent_transfer"})
    total_minutes = sum(item["minutes"] for item in phases)
    recent_errors = db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == user.id, ExerciseAttempt.correct == False).order_by(ExerciseAttempt.created_at.desc()).limit(100).all()
    error_counts = {}
    for attempt in recent_errors:
        error_counts[attempt.topic] = error_counts.get(attempt.topic, 0) + 1
    mistake_patterns = [{"topic": topic, "count": count} for topic, count in sorted(error_counts.items(), key=lambda item: (-item[1], item[0]))[:5] if count >= 2]
    retained = [item for item in mastery if retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now)) >= 70]
    at_risk = [item for item in mastery if retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now)) < 50]
    return {
        "due_count": due_count,
        "due_topics": [{"topic": item.topic, "mastery": round(item.mastery), "retention": retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now))} for item in due[:5]],
        "mastery": [{
            "topic": item.topic,
            "mastery": round(item.mastery),
            "retention": retention_score(item.mastery, item.stability_days or 1, _days_overdue(item.next_review_at, now)),
            "attempts": item.attempts,
            "lapses": item.lapse_count or 0,
        } for item in mastery[:8]],
        "retention_summary": {"learned": len(mastery), "retained": len(retained), "at_risk": len(at_risk)},
        "mistake_patterns": mistake_patterns,
        "assessment": assessment,
        "next_lesson": ({
            "id": next_lesson.id,
            "topic": next_lesson.topic,
            "title": next_content.get("title", next_lesson.topic),
            "level": next_lesson.level,
            "minutes": next_lesson.estimated_time or 12,
            "module_title": next_content.get("module_title"),
            "module_step": next_content.get("module_step") or next_content.get("day"),
            "module_size": next_content.get("module_size"),
            "can_do": next_content.get("can_do") or next_content.get("objective"),
            "scenario": next_content.get("scenario"),
            "reason": "review_due" if next_lesson.topic in {item.topic for item in due} else ("weakest_ready_skill" if mastery else "first_step"),
            "blocked_by": lesson_blockers(next_lesson, plan, completed_ids, mastery_map),
        } if next_lesson else None),
        "session": {
            "phases": phases,
            "minutes": total_minutes,
            "explanation": "review_repair_learn_speak" if review_count else "repair_learn_speak",
        },
    }


@router.get("/reviews/{user_id}")
async def reviews(user_id: int, lang: str | None = None, db: Session = Depends(get_db), authenticated_id: int = Depends(telegram_user_id)):
    assert_owner(authenticated_id, user_id)
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    rows = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.next_review_at <= now).order_by(TopicMastery.mastery.asc()).limit(2).all()
    production_attempts = db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == user.id, ExerciseAttempt.assessment.isnot(None)).order_by(ExerciseAttempt.created_at.desc()).limit(100).all()
    assessment = assessment_insights(production_attempts)
    repair_focus = assessment["priority_topics"][0] if assessment["priority_topics"] else None
    if repair_focus and repair_focus["score"] < 70 and repair_focus["topic"] not in {row.topic for row in rows}:
        repair_mastery = db.query(TopicMastery).filter(TopicMastery.user_id == user.id, TopicMastery.topic == repair_focus["topic"]).first()
        if repair_mastery:
            rows = [repair_mastery, *rows][:2]
    result = []
    for row in rows:
        lesson = db.query(Lesson).filter(Lesson.topic == row.topic, Lesson.is_active == True).first()
        content = localize_lesson_content(normalize_lesson_content(lesson.content or {}, lesson.topic, lesson.level), normalize_language(lang or user.language_code)) if lesson else {}
        exercises = content.get("exercises", [])
        if lesson and exercises:
            # Повторение проверяет самостоятельное извлечение, а не этап с подсказкой.
            repair_dimension = repair_focus["dimension"] if repair_focus and row.topic == repair_focus["topic"] else None
            preferred_types = {"grammar": {"error_repair", "transform"}, "task_completion": {"dialogue", "production"}, "vocabulary": {"dialogue", "production"}, "coherence": {"dialogue", "production"}, "register": {"dialogue", "production"}}.get(repair_dimension, set())
            delayed_review = content.get("delayed_review") or {}
            final_index = next((index for index, item in enumerate(exercises) if item.get("mission_role") == "final"), None)
            exercise_index = final_index if delayed_review.get("method") == "changed_context_retrieval" and final_index is not None else next((index for index, item in enumerate(exercises) if item.get("type") in preferred_types), 1 if len(exercises) > 1 else 0)
            exercise = exercises[exercise_index]
            attempts = int(row.attempts or 0)
            evidence_status = "not_enough_evidence" if attempts < 2 else "building" if attempts < 4 else "retained" if row.mastery >= 70 else "needs_review"
            result.append({"topic": row.topic, "mastery": round(row.mastery), "attempts": attempts, "evidence_status": evidence_status, "can_do": content.get("can_do") or content.get("objective"), "review_reason": delayed_review.get("reason"), "lesson_id": lesson.id, "exercise_index": exercise_index, "question": delayed_review.get("prompt") or exercise.get("question", ""), "type": exercise.get("type", "fill"), "options": exercise.get("options", []), "tokens": exercise.get("tokens", []), "conversation_turns": exercise.get("conversation_turns", []), "target_patterns": exercise.get("target_patterns", []), "repair_dimension": repair_dimension, "repair_score": repair_focus["score"] if repair_dimension else None})
    return {"reviews": result, "assessment": assessment}
