from app.services.skill_graph import blocked_by


def curriculum_track_for_level(level: str | None) -> str:
    return "B1" if (level or "").upper() in {"B1", "B2", "C1", "C2"} else "foundation"


def filter_roadmap_for_level(lessons, level: str | None):
    """Choose one coherent route while retaining a fallback for older databases."""
    requested = curriculum_track_for_level(level)
    selected = [
        lesson for lesson in lessons
        if ((lesson.content or {}).get("track") or "foundation") == requested
    ]
    if selected:
        return selected
    return [lesson for lesson in lessons if ((lesson.content or {}).get("track") or "foundation") == "foundation"]


def roadmap_order(lesson) -> int:
    content = lesson.content if isinstance(lesson.content, dict) else {}
    return int(content.get("day") or 999)


def lesson_blockers(lesson, lessons, completed_ids: set[int], mastery: dict[str, float]) -> list[str]:
    """Return explainable blockers for one stable, sequential curriculum."""
    if lesson.id in completed_ids:
        return []
    blockers = list(blocked_by(lesson.topic, mastery))
    earlier_same_skill = next((
        item for item in lessons
        if item.topic == lesson.topic
        and item.id not in completed_ids
        and roadmap_order(item) < roadmap_order(lesson)
    ), None)
    if earlier_same_skill:
        blockers.append("previous_step")
    return blockers


def select_recommended_lesson(lessons, completed_ids: set[int], mastery: dict[str, float], weak_points: dict):
    """Adapt the next action without renumbering or reshuffling the route."""
    candidates = [
        lesson for lesson in lessons
        if lesson.id not in completed_ids
        and not lesson_blockers(lesson, lessons, completed_ids, mastery)
    ]
    if not candidates:
        return next((lesson for lesson in lessons if lesson.id not in completed_ids), None)

    def priority(lesson):
        weakness = sum(float(weak_points.get(tag, 0) or 0) for tag in (lesson.weak_point_tags or []))
        known_mastery = float(mastery.get(lesson.topic, 50))
        return (-weakness, known_mastery, roadmap_order(lesson))

    return min(candidates, key=priority)
