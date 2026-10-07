"""DeutschIQ 86 privacy-safe learning and production analytics."""
from collections import Counter, defaultdict


FUNNEL = (
    ("diagnostic_completed", "Diagnostic"),
    ("today_viewed", "Today"),
    ("lesson_started", "Lesson started"),
    ("exercise_answered", "Exercise answered"),
    ("lesson_completed", "Lesson completed"),
    ("review_started", "Review started"),
    ("review_completed", "Review completed"),
)


def learning_analytics(events, attempts, mastery_rows) -> dict:
    users = defaultdict(set)
    event_counts = Counter()
    answer = {"first": [0, 0], "retry": [0, 0], "review": [0, 0]}
    tutor_modes = Counter()
    for event in events:
        event_counts[event.event_name] += 1
        users[event.event_name].add(int(event.user_id))
        props = event.properties or {}
        if event.event_name == "exercise_answered":
            bucket = "retry" if bool(props.get("retry")) else "first"
            answer[bucket][0] += 1
            answer[bucket][1] += int(bool(props.get("correct")))
        elif event.event_name == "review_answered":
            answer["review"][0] += 1
            answer["review"][1] += int(bool(props.get("correct")))
        elif event.event_name == "tutor_answered":
            tutor_modes[str(props.get("mode") or "unknown")] += 1

    funnel = []
    previous = None
    for event_name, label in FUNNEL:
        count = len(users[event_name])
        conversion = round(count / previous * 100) if previous else None
        funnel.append({"event": event_name, "label": label, "users": count, "from_previous": conversion})
        previous = count

    def rate(pair):
        total, correct = pair
        return round(correct / total * 100) if total else None

    repaired = event_counts["mission_repair_completed"]
    repair_success = sum(
        int(bool((event.properties or {}).get("repaired")))
        for event in events if event.event_name == "mission_repair_completed"
    )
    at_risk = sum(float(row.mastery) >= 70 and getattr(row, "next_review_at", None) is not None for row in mastery_rows)
    return {
        "funnel": funnel,
        "effectiveness": {
            "first_try": {"answers": answer["first"][0], "accuracy": rate(answer["first"])},
            "supported_retry": {"answers": answer["retry"][0], "accuracy": rate(answer["retry"])},
            "delayed_retrieval": {"answers": answer["review"][0], "accuracy": rate(answer["review"])},
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
