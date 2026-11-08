"""DeutschIQ 86 privacy-safe learning and production analytics."""
from collections import Counter, defaultdict
from datetime import timedelta


FUNNEL = (
    ("diagnostic_completed", "Diagnostic"),
    ("today_viewed", "Today"),
    ("lesson_started", "Lesson started"),
    ("exercise_answered", "Exercise answered"),
    ("lesson_completed", "Lesson completed"),
    ("review_started", "Review started"),
    ("review_completed", "Review completed"),
)


def telemetry_true(value) -> bool:
    """Accept real booleans and explicit true/false telemetry values only."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1"}
    return False


def learning_analytics(events, attempts, mastery_rows) -> dict:
    users = defaultdict(set)
    event_times = defaultdict(lambda: defaultdict(list))
    event_counts = Counter()
    answer = {"first": [0, 0], "retry": [0, 0], "review": [0, 0]}
    tutor_modes = Counter()
    for event in events:
        event_counts[event.event_name] += 1
        users[event.event_name].add(int(event.user_id))
        timestamp = getattr(event, "created_at", None)
        if timestamp is not None:
            event_times[event.event_name][int(event.user_id)].append(timestamp)
        props = event.properties or {}
        if event.event_name == "exercise_answered":
            bucket = "retry" if telemetry_true(props.get("retry")) else "first"
            answer[bucket][0] += 1
            answer[bucket][1] += int(telemetry_true(props.get("correct")))
        elif event.event_name == "review_answered":
            answer["review"][0] += 1
            answer["review"][1] += int(telemetry_true(props.get("correct")))
        elif event.event_name == "tutor_answered":
            tutor_modes[str(props.get("mode") or "unknown")] += 1

    funnel = []
    previous_users = None
    previous_event = None
    for event_name, label in FUNNEL:
        current_users = users[event_name]
        count = len(current_users)
        # Count only learners who reached the next step after the prior step.
        # For legacy events without timestamps, retain the overlap estimate.
        progressed = 0
        if previous_users:
            for user_id in current_users & previous_users:
                before = event_times[previous_event][user_id]
                after = event_times[event_name][user_id]
                if not before or not after or any(a > b for a in after for b in before):
                    progressed += 1
        conversion = round(progressed / len(previous_users) * 100) if previous_users else None
        funnel.append({"event": event_name, "label": label, "users": count, "from_previous": conversion})
        previous_users = current_users
        previous_event = event_name

    def rate(pair):
        total, correct = pair
        return round(correct / total * 100) if total else None

    # Observed delayed topic attempts are distinct from client-reported review answers.
    # Count only the first follow-up per learner/topic, at least 24h after baseline.
    topic_attempts = defaultdict(list)
    for attempt in attempts:
        timestamp = getattr(attempt, "created_at", None)
        topic = getattr(attempt, "topic", None)
        user_id = getattr(attempt, "user_id", None)
        if timestamp is not None and topic and user_id is not None:
            topic_attempts[(int(user_id), str(topic))].append(attempt)
    delayed_followups = []
    for rows in topic_attempts.values():
        rows.sort(key=lambda row: row.created_at)
        baseline = rows[0].created_at
        followup = next((row for row in rows[1:] if row.created_at - baseline >= timedelta(hours=24)), None)
        if followup is not None:
            delayed_followups.append(followup)

    # Independent first qualifying follow-up for each minimum elapsed window.
    # Windows are cumulative (>= 1, >= 3, >= 7 days), not exclusive buckets.
    followup_windows = {}
    for days in (1, 3, 7):
        observed = []
        for rows in topic_attempts.values():
            baseline = rows[0].created_at
            followup = next((row for row in rows[1:] if row.created_at - baseline >= timedelta(days=days)), None)
            if followup is not None:
                observed.append(followup)
        followup_windows[str(days)] = {
            "cohorts": len(observed),
            "accuracy": round(sum(bool(row.correct) for row in observed) / len(observed) * 100) if observed else None,
        }

    repaired = event_counts["mission_repair_completed"]
    repair_success = sum(
        int(telemetry_true((event.properties or {}).get("repaired")))
        for event in events if event.event_name == "mission_repair_completed"
    )
    at_risk = sum(float(row.mastery) >= 70 and getattr(row, "next_review_at", None) is not None for row in mastery_rows)
    return {
        "funnel": funnel,
        "effectiveness": {
            "first_try": {"answers": answer["first"][0], "accuracy": rate(answer["first"])},
            "supported_retry": {"answers": answer["retry"][0], "accuracy": rate(answer["retry"])},
            "delayed_retrieval": {"answers": answer["review"][0], "accuracy": rate(answer["review"])},
            "delayed_topic_followup": {"cohorts": len(delayed_followups), "accuracy": round(sum(bool(row.correct) for row in delayed_followups) / len(delayed_followups) * 100) if delayed_followups else None, "minimum_gap_hours": 24},
            "delayed_topic_windows": followup_windows,
            "mission_repair": {"attempts": repaired, "success_rate": round(repair_success / repaired * 100) if repaired else None},
            "mastery_topics": len(mastery_rows),
            "scheduled_retention_topics": at_risk,
        },
        "tutor": {
            "answers": event_counts["tutor_answered"],
            "ai": tutor_modes["ai"],
            "fallback": tutor_modes["local"],
            "fallback_rate": round(tutor_modes["local"] / event_counts["tutor_answered"] * 100) if event_counts["tutor_answered"] else None,
        },
    }


def production_alerts(event_summary: dict, learning: dict) -> list[dict]:
    reliability = event_summary.get("reliability", {})
    serious = int(event_summary.get("reliability_detail", {}).get("serious_errors", 0))
    alerts = []
    if serious:
        alerts.append({"severity": "critical", "signal": "serious_errors", "count": serious, "message": "Network/server failures, client crashes or reload loops need investigation."})
    if int(reliability.get("api_slow", 0)) >= 3:
        alerts.append({"severity": "warning", "signal": "api_slow", "count": int(reliability["api_slow"]), "message": "Repeated API responses exceeded the client slow-request threshold."})
    fallback_rate = learning.get("tutor", {}).get("fallback_rate")
    if fallback_rate is not None and learning["tutor"]["answers"] >= 5 and fallback_rate >= 20:
        alerts.append({"severity": "warning", "signal": "tutor_fallback", "count": learning["tutor"]["fallback"], "message": "AI Tutor is falling back locally in at least 20% of measured replies."})
    return alerts
