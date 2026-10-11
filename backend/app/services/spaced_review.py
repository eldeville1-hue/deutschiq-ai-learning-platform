"""Timezone-aware spaced-review scheduling for German grammar skills."""

from datetime import datetime, timedelta, timezone

REVIEW_INTERVAL_DAYS = (1, 3, 7, 14, 30)


def next_review(previous: dict | None, correct: bool, answered_at: datetime) -> dict:
    """Advance after correct recall; reset after a mistake."""
    if not isinstance(correct, bool):
        raise ValueError("correct must be boolean")
    if answered_at.tzinfo is None or answered_at.utcoffset() is None:
        raise ValueError("answered_at must have a timezone")
    previous = previous or {}
    old_step = previous.get("step", -1)
    if not isinstance(old_step, int) or isinstance(old_step, bool):
        old_step = -1
    step = min(max(old_step + 1, 0), len(REVIEW_INTERVAL_DAYS) - 1) if correct else 0
    due_at = answered_at.astimezone(timezone.utc) + timedelta(days=REVIEW_INTERVAL_DAYS[step])
    return {"step": step, "due_at": due_at.isoformat(), "interval_days": REVIEW_INTERVAL_DAYS[step]}


def review_is_due(state: dict, now: datetime) -> bool:
    """Ignore malformed or naive due dates."""
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must have a timezone")
    if not isinstance(state, dict) or not isinstance(state.get("due_at"), str):
        return False
    try:
        due_at = datetime.fromisoformat(state["due_at"].replace("Z", "+00:00"))
        if due_at.tzinfo is None or due_at.utcoffset() is None:
            return False
    except ValueError:
        return False
    return due_at <= now



def due_review_skills(states: dict, now: datetime, available_skills: set[str] | None = None,
                      limit: int = 5) -> list[str]:
    """Select overdue skills from caller-supplied per-user review states."""
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must have a timezone")
    if not isinstance(states, dict) or not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        return []
    due = []
    for skill, state in states.items():
        if not isinstance(skill, str) or not skill.strip():
            continue
        if available_skills is not None and skill not in available_skills:
            continue
        if review_is_due(state, now):
            timestamp = datetime.fromisoformat(state["due_at"].replace("Z", "+00:00"))
            due.append((timestamp, skill))
    return [skill for _, skill in sorted(due)[:limit]]
