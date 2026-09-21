"""Privacy-safe aggregation helpers for the internal beta control center."""
from collections import Counter, defaultdict


RELIABILITY_EVENTS = {"api_failed", "api_slow", "client_error", "reload_loop_detected", "microphone_failed"}


def summarize_events(events) -> dict:
    counts = Counter(item.event_name for item in events)
    users_by_event: dict[str, set[int]] = defaultdict(set)
    modes: dict[str, dict[str, int]] = defaultdict(lambda: {"answers": 0, "correct": 0})
    reliability = Counter()
    feedback = []
    for item in events:
        users_by_event[item.event_name].add(int(item.user_id))
        properties = item.properties or {}
        if item.event_name in RELIABILITY_EVENTS:
            reliability[item.event_name] += 1
        if item.event_name == "exercise_answered":
            mode = str(properties.get("learning_mode") or "unknown")
            modes[mode]["answers"] += 1
            modes[mode]["correct"] += int(bool(properties.get("correct")))
        if item.event_name == "beta_feedback" and properties.get("message"):
            feedback.append({
                "message": str(properties.get("message"))[:800],
                "language": str(properties.get("language") or "unknown")[:8],
                "page": str(properties.get("page") or "unknown")[:120],
                "created_at": item.created_at.isoformat() if item.created_at else None,
            })
    mode_rows = [
        {"mode": mode, **values, "accuracy": round(values["correct"] / values["answers"] * 100) if values["answers"] else None}
        for mode, values in sorted(modes.items())
    ]
    return {
        "counts": dict(counts),
        "unique_users": {name: len(values) for name, values in users_by_event.items()},
        "reliability": dict(reliability),
        "learning_modes": mode_rows,
        "feedback": list(reversed(feedback[-30:])),
    }


def exercise_health(attempts, lesson_topics: dict[int, str]) -> list[dict]:
    grouped = defaultdict(lambda: {"attempts": 0, "correct": 0, "users": set()})
    for item in attempts:
        key = (int(item.lesson_id), int(item.exercise_index))
        grouped[key]["attempts"] += 1
        grouped[key]["correct"] += int(bool(item.correct))
        grouped[key]["users"].add(int(item.user_id))
    rows = []
    for (lesson_id, exercise_index), values in grouped.items():
        attempts_count = values["attempts"]
        accuracy = round(values["correct"] / attempts_count * 100) if attempts_count else 0
        status = "too_hard" if attempts_count >= 5 and accuracy < 40 else "too_easy" if attempts_count >= 5 and accuracy > 92 else "healthy"
        rows.append({
            "lesson_id": lesson_id, "topic": lesson_topics.get(lesson_id, "unknown"),
            "exercise_index": exercise_index, "attempts": attempts_count,
            "learners": len(values["users"]), "accuracy": accuracy, "status": status,
        })
    return sorted(rows, key=lambda row: (-int(row["attempts"]), int(row["accuracy"])))[:40]

