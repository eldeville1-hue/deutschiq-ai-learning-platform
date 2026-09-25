from app.services.skill_graph import blocked_by

CEFR_TRACKS = ("A1", "A2", "B1", "B2")


def normalize_cefr(level: str | None) -> str:
    value = (level or "A1").upper().strip()[:2]
    return value if value in CEFR_TRACKS else ("B2" if value in {"C1", "C2"} else "A1")


def track_access(track: str, current_level: str | None) -> str:
    """Return the learner-facing state for a CEFR track."""
    if track == "C1":
        return "coming_soon"
    if track not in CEFR_TRACKS:
        return "locked"
    current = normalize_cefr(current_level)
    requested_rank = CEFR_TRACKS.index(track)
    current_rank = CEFR_TRACKS.index(current)
    if requested_rank < current_rank:
        return "review"
    if requested_rank == current_rank:
        return "active"
    return "locked"


def next_cefr_track(level: str | None) -> str | None:
    current = normalize_cefr(level)
    index = CEFR_TRACKS.index(current)
    return CEFR_TRACKS[index + 1] if index + 1 < len(CEFR_TRACKS) else None


def curriculum_track_for_level(level: str | None) -> str:
    # Accept display variants such as A1+ without letting presentation labels
    # accidentally route a learner into another CEFR course.
    normalized = normalize_cefr(level)
    if normalized in {"B2", "C1", "C2"}:
        return "B2"
    if normalized == "B1":
        return "B1"
    return "A2" if normalized == "A2" else "A1"


def filter_roadmap_for_level(lessons, level: str | None):
    """Choose one coherent route while retaining a fallback for older databases."""
    requested = curriculum_track_for_level(level)
    selected = [
        lesson for lesson in lessons
        if ((lesson.content or {}).get("track") or "foundation") == requested
    ]
    if selected:
        return selected
    fallback_order = {
        "A1": ("foundation",),
        "A2": ("A1", "foundation"),
        "B1": ("A2", "A1", "foundation"),
        "B2": ("B1", "A2", "A1", "foundation"),
    }
    for fallback in fallback_order.get(requested, ("foundation",)):
        fallback_lessons = [lesson for lesson in lessons if ((lesson.content or {}).get("track") or "foundation") == fallback]
        if fallback_lessons:
            return fallback_lessons
    return []


def roadmap_order(lesson) -> int:
    content = lesson.content if isinstance(lesson.content, dict) else {}
    return int(content.get("day") or 999)


def lesson_blockers(lesson, lessons, completed_ids: set[int], mastery: dict[str, float]) -> list[str]:
    """Return explainable blockers for one stable, sequential curriculum."""
    if lesson.id in completed_ids:
        return []
    blockers = list(blocked_by(lesson.topic, mastery))
    content = lesson.content if isinstance(lesson.content, dict) else {}
    track = content.get("track")
    for prerequisite in content.get("prerequisites") or []:
        prerequisite_lessons = [
            item for item in lessons
            if item.topic == prerequisite and (item.content or {}).get("track") == track
        ]
        completed = any(item.id in completed_ids for item in prerequisite_lessons)
        demonstrated = float(mastery.get(prerequisite, 0) or 0) >= 70
        if not completed and not demonstrated:
            blockers.append("previous_step")
            break
    earlier_same_skill = next((
        item for item in lessons
        if item.topic == lesson.topic
        and item.id not in completed_ids
        and roadmap_order(item) < roadmap_order(lesson)
    ), None)
    if earlier_same_skill:
        blockers.append("previous_step")
    return list(dict.fromkeys(blockers))


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
