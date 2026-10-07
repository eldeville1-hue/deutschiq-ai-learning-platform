from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.services.tutor_context import build_tutor_learning_context, tutor_context_prompt


def mastery(topic, score, stability=4, review_at=None):
    return SimpleNamespace(topic=topic, mastery=score, stability_days=stability, next_review_at=review_at)


def attempt(topic, correct=True, assessment=None):
    return SimpleNamespace(topic=topic, correct=correct, assessment=assessment)


def lesson(lesson_id, topic, day):
    return SimpleNamespace(id=lesson_id, topic=topic, content={"day": day, "track": "B1", "prerequisites": []}, weak_point_tags=[topic])


def test_tutor_context_uses_today_route_due_review_and_recurring_errors():
    now = datetime(2026, 10, 7, 12, tzinfo=timezone.utc)
    rows = [
        mastery("word_order", 78, 3, now - timedelta(days=4)),
        mastery("connectors", 62, 10, now + timedelta(days=3)),
    ]
    attempts = [attempt("word_order", False), attempt("word_order", False), attempt("connectors", True)]
    context = build_tutor_learning_context(
        level="B1", mastery_rows=rows, recent_attempts=attempts,
        plan=[lesson(1, "word_order", 1), lesson(2, "connectors", 2)],
        completed_ids={1}, weak_points={}, now=now,
    )
    assert context["today_topic"] == "connectors"
    assert context["due_reviews"] == ["word_order"]
    assert context["recurring_errors"] == [{"topic": "word_order", "count": 2}]
    assert context["weak_skills"][0]["topic"] == "word_order"


def test_tutor_context_exposes_specific_production_repair():
    context = build_tutor_learning_context(
        level="B2",
        mastery_rows=[mastery("argumentation", 70)],
        recent_attempts=[
            attempt("argumentation", True, {"dimensions": {"task_completion": 82, "grammar": 48, "vocabulary": 86, "coherence": 75, "register": 74}}),
            attempt("argumentation", True, {"dimensions": {"task_completion": 84, "grammar": 52, "vocabulary": 88, "coherence": 76, "register": 76}}),
        ],
        plan=[lesson(3, "argumentation", 1)], completed_ids=set(), weak_points={},
    )
    assert context["production_repair"]["topic"] == "argumentation"
    assert context["production_repair"]["dimension"] == "grammar"
    assert context["production_repair"]["score"] == 50
    prompt = tutor_context_prompt(context)
    assert "argumentation: grammar 50/100" in prompt


def test_single_error_is_not_misrepresented_as_recurring_pattern():
    context = build_tutor_learning_context(
        level="A2", mastery_rows=[mastery("articles", 55)],
        recent_attempts=[attempt("articles", False)],
        plan=[lesson(4, "articles", 1)], completed_ids=set(), weak_points={},
    )
    assert context["recurring_errors"] == []
