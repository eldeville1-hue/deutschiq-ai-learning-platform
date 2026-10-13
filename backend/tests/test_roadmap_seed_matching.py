from types import SimpleNamespace

from seed_30_day_plan import find_roadmap_lesson


def lesson(lesson_id, day, track=None, topic="shared"):
    content = {"day": day}
    if track is not None:
        content["track"] = track
    return SimpleNamespace(id=lesson_id, topic=topic, content=content)


def test_roadmap_prefers_legacy_day_without_touching_cefr():
    cefr = lesson(1, 10, "A2")
    roadmap = lesson(2, 10)
    assert find_roadmap_lesson([cefr, roadmap], 10, "shared") is roadmap


def test_roadmap_does_not_match_cefr_by_topic():
    cefr = lesson(1, 10, "B1", "same-topic")
    assert find_roadmap_lesson([cefr], 10, "same-topic") is None


def test_roadmap_falls_back_to_legacy_topic():
    legacy = lesson(3, 5, topic="old-title")
    assert find_roadmap_lesson([lesson(1, 5, "A1"), legacy], 11, "old-title") is legacy
