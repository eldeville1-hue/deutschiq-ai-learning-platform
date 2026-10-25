"""Regression coverage for duplicate 30-day roadmap records.

A duplicate day is not necessarily a disposable lesson: existing learner
progress may reference either ID. Audit before any destructive cleanup.
"""
from types import SimpleNamespace

from seed_30_day_plan import find_roadmap_lesson


def lesson(lesson_id, day, track=None, topic="word_order"):
    return SimpleNamespace(
        id=lesson_id, topic=topic,
        content={"day": day, **({"track": track} if track else {})},
    )


def duplicate_roadmap_days(lessons):
    days = {}
    for item in lessons:
        content = item.content if isinstance(item.content, dict) else {}
        if content.get("track") in {"A1", "A2", "B1", "B2"}:
            continue
        day = content.get("day")
        if isinstance(day, int) and 1 <= day <= 30:
            days.setdefault(day, []).append(item.id)
    return {day: ids for day, ids in days.items() if len(ids) > 1}


def test_detects_legacy_duplicate_without_counting_cefr_days():
    lessons = [lesson(10, 10), lesson(84, 10), lesson(110, 10, "A2")]
    assert duplicate_roadmap_days(lessons) == {10: [10, 84]}


def test_legacy_day_match_does_not_select_cefr_duplicate():
    lessons = [lesson(110, 10, "A2"), lesson(84, 10)]
    assert find_roadmap_lesson(lessons, 10, "word_order").id == 84


def test_duplicate_report_does_not_modify_lesson_ids():
    lessons = [lesson(10, 10), lesson(84, 10)]
    assert duplicate_roadmap_days(lessons) == {10: [10, 84]}
    assert [item.id for item in lessons] == [10, 84]
