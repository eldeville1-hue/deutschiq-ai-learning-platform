"""Privacy-safe aggregation helpers for the internal beta control center."""
from collections import Counter, defaultdict
from datetime import timedelta
import hashlib
import hmac


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
                "category": str(properties.get("category") or properties.get("kind") or "feedback")[:40],
                "lesson_id": properties.get("lesson_id"),
                "exercise_index": properties.get("exercise_index"),
                "exercise_type": str(properties.get("exercise_type") or "")[:40] or None,
                "topic": str(properties.get("topic") or "")[:100] or None,
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


def retention_cohorts(enrollments, sessions, now) -> dict:
    sessions_by_user = defaultdict(list)
    for item in sessions:
        if item.started_at:
            sessions_by_user[int(item.user_id)].append(item.started_at.replace(tzinfo=None))
    result = {}
    for day in (1, 3, 7):
        eligible = [item for item in enrollments if item.joined_at and item.joined_at.replace(tzinfo=None) <= now - timedelta(days=day)]
        retained = sum(any(moment >= item.joined_at.replace(tzinfo=None) + timedelta(days=day) for moment in sessions_by_user[int(item.user_id)]) for item in eligible)
        result[f"d{day}"] = {"eligible": len(eligible), "retained": retained, "rate": round(retained / len(eligible) * 100) if eligible else None}
    return result


def tester_alias(user_id: int, secret_key: str) -> str:
    digest = hmac.new(secret_key.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()[:8].upper()
    return f"T-{digest}"


def tester_progress(enrollments, users, invites, sessions, events, secret_key: str) -> list[dict]:
    users_by_id = {item.id: item for item in users}
    invite_by_id = {item.id: item for item in invites}
    sessions_by_user = defaultdict(list)
    events_by_user = defaultdict(list)
    for session in sessions:
        sessions_by_user[session.user_id].append(session)
    for event in events:
        events_by_user[event.user_id].append(event)
    rows = []
    for enrollment in enrollments:
        user = users_by_id.get(enrollment.user_id)
        user_sessions = sessions_by_user[enrollment.user_id]
        user_events = events_by_user[enrollment.user_id]
        activity = [item.created_at for item in user_events if item.created_at] + [item.started_at for item in user_sessions if item.started_at]
        invite = invite_by_id.get(enrollment.invite_id)
        rows.append({
            "tester": tester_alias(enrollment.user_id, secret_key),
            "invite": invite.label if invite else "unknown",
            "language": (user.language_code if user else None) or "unknown",
            "joined_at": enrollment.joined_at.isoformat() if enrollment.joined_at else None,
            "onboarded": bool(enrollment.consent and enrollment.goal),
            "diagnostic_completed": bool(user and user.diagnostic_completed),
            "lessons_started": len(user_sessions),
            "lessons_completed": sum(item.status in {"passed", "practice_needed"} for item in user_sessions),
            "feedback_count": sum(item.event_name == "beta_feedback" for item in user_events),
            "last_activity_at": max(activity).isoformat() if activity else None,
        })
    return sorted(rows, key=lambda item: item["joined_at"] or "", reverse=True)
