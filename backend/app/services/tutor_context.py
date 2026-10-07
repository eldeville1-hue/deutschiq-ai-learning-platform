"""Compact, testable learner context for the DeutschIQ Tutor."""
from collections import Counter
from datetime import datetime, timezone

from app.services.assessment_insights import assessment_insights
from app.services.learning_engine import adaptive_priority_score
from app.services.learning_route import select_recommended_lesson


def days_overdue(review_at, now=None):
    if not review_at:
        return 0.0
    now = now or datetime.now(timezone.utc)
    if review_at.tzinfo is None:
        review_at = review_at.replace(tzinfo=timezone.utc)
    return max(0.0, (now - review_at).total_seconds() / 86400)


def build_tutor_learning_context(*, level, mastery_rows, recent_attempts, plan, completed_ids, weak_points, now=None):
    now = now or datetime.now(timezone.utc)
    mastery_map = {row.topic: float(row.mastery) for row in mastery_rows}
    retention_map = {
        row.topic: adaptive_priority_score(row.mastery, row.stability_days or 1, days_overdue(row.next_review_at, now))
        for row in mastery_rows
    }
    next_lesson = select_recommended_lesson(plan, completed_ids, mastery_map, weak_points or {}, retention_map)
    due = [row for row in mastery_rows if row.next_review_at and ((row.next_review_at.replace(tzinfo=timezone.utc) if row.next_review_at.tzinfo is None else row.next_review_at) <= now)]
    errors = [attempt for attempt in recent_attempts if not attempt.correct]
    recurring = Counter(attempt.topic for attempt in errors)
    assessment = assessment_insights([attempt for attempt in recent_attempts if getattr(attempt, "assessment", None)])
    repair = assessment["priority_topics"][0] if assessment["priority_topics"] else None
    weakest = sorted(mastery_rows, key=lambda row: retention_map.get(row.topic, 100))[:4]
    return {
        "level": level,
        "today_topic": next_lesson.topic if next_lesson else None,
        "today_lesson_id": next_lesson.id if next_lesson else None,
        "due_reviews": [row.topic for row in sorted(due, key=lambda row: retention_map.get(row.topic, 100))[:3]],
        "weak_skills": [{"topic": row.topic, "mastery": round(row.mastery), "retention": retention_map.get(row.topic)} for row in weakest],
        "recurring_errors": [{"topic": topic, "count": count} for topic, count in recurring.most_common(4) if count >= 2],
        "production_repair": repair if repair and repair["score"] < 70 else None,
    }


def tutor_context_prompt(context):
    weak = ", ".join(f'{item["topic"]} {item["mastery"]}% (retention {item["retention"]}%)' for item in context["weak_skills"]) or "none"
    recurring = ", ".join(f'{item["topic"]} x{item["count"]}' for item in context["recurring_errors"]) or "none"
    repair = context["production_repair"]
    repair_text = f'{repair["topic"]}: {repair["dimension"]} {repair["score"]}/100' if repair else "none"
    return (
        f'Current learning target: {context["today_topic"] or "none"}\n'
        f'Due retrieval: {", ".join(context["due_reviews"]) or "none"}\n'
        f'Weak retained skills: {weak}\n'
        f'Recurring recent errors: {recurring}\n'
        f'Production repair priority: {repair_text}'
    )
