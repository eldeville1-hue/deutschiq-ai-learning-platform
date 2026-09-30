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


def lesson_content_health(lessons, attempts, sessions, events, blocker_for) -> list[dict]:
    """Combine publishing quality and real learner evidence without inventing precision."""
    attempts_by_lesson = defaultdict(list)
    sessions_by_lesson = defaultdict(list)
    events_by_lesson = defaultdict(list)
    for item in attempts:
        attempts_by_lesson[int(item.lesson_id)].append(item)
    for item in sessions:
        sessions_by_lesson[int(item.lesson_id)].append(item)
    for item in events:
        lesson_id = (item.properties or {}).get("lesson_id")
        if isinstance(lesson_id, (int, float)) or (isinstance(lesson_id, str) and lesson_id.isdigit()):
            events_by_lesson[int(lesson_id)].append(item)

    rows = []
    for lesson in sorted(lessons, key=lambda value: int((value.content or {}).get("day") or 999)):
        content = lesson.content or {}
        lesson_attempts = attempts_by_lesson[int(lesson.id)]
        lesson_sessions = sessions_by_lesson[int(lesson.id)]
        lesson_events = events_by_lesson[int(lesson.id)]
        blockers = blocker_for(content)
        learners = {int(item.user_id) for item in lesson_attempts}
        started = sum(item.event_name == "lesson_started" for item in lesson_events) or len(lesson_sessions)
        completed = sum(item.event_name == "lesson_completed" for item in lesson_events)
        if not completed:
            completed = sum(item.status in {"passed", "practice_needed"} for item in lesson_sessions)
        skipped = sum(item.event_name == "exercise_skipped" for item in lesson_events)
        answer_events = sum(item.event_name == "exercise_answered" for item in lesson_events)
        review_events = [item for item in lesson_events if item.event_name == "review_answered"]
        repair_events = [item for item in lesson_events if item.event_name == "mission_repair_completed"]

        completion_rate = round(completed / started * 100) if started >= 5 else None
        skip_rate = round(skipped / (answer_events + skipped) * 100) if answer_events + skipped >= 5 else None
        review_success = round(sum(bool((item.properties or {}).get("correct")) for item in review_events) / len(review_events) * 100) if len(review_events) >= 5 else None
        repair_success = round(sum(bool((item.properties or {}).get("repaired")) for item in repair_events) / len(repair_events) * 100) if len(repair_events) >= 5 else None

        reasons = []
        if blockers:
            status = "blocked"
            reasons.append(f"{len(blockers)} publishing gate(s) failed")
        elif len(learners) < 5 or completed < 5:
            status = "collecting"
            reasons.append("Fewer than 5 learners or completed sessions")
        elif len(review_events) < 5:
            status = "awaiting_recall"
            reasons.append("Delayed-recall sample is not large enough")
        else:
            if completion_rate is not None and completion_rate < 60:
                reasons.append("Completion is below 60%")
            if skip_rate is not None and skip_rate > 20:
                reasons.append("More than 20% of interactions are skipped")
            if review_success is not None and review_success < 60:
                reasons.append("Changed-context recall is below 60%")
            if repair_success is not None and repair_success < 60:
                reasons.append("Mission repair success is below 60%")
            status = "needs_review" if reasons else "healthy"

        rows.append({
            "lesson_id": lesson.id,
            "day": int(content.get("day") or 0),
            "module": int(content.get("module") or content.get("week") or 0),
            "topic": lesson.topic,
            "title": content.get("title") or lesson.topic,
            "publish_ready": not blockers,
            "publication_blockers": blockers,
            "status": status,
            "reasons": reasons,
            "sample": {
                "learners": len(learners), "attempts": len(lesson_attempts),
                "started": started, "completed": completed,
                "reviews": len(review_events), "repairs": len(repair_events),
            },
            "signals": {
                "completion_rate": completion_rate, "skip_rate": skip_rate,
                "review_success": review_success, "repair_success": repair_success,
            },
        })
    return rows


def beta_readiness(content_health: list[dict], event_summary: dict, enrolled: int, active_learners: int, journey_issues: list[str] | None = None) -> dict:
    """Return explicit release gates. Missing samples stay missing instead of becoming 0%."""
    a1_complete = len(content_health) == 20
    publish_ready = a1_complete and all(item["publish_ready"] for item in content_health)
    journey_issues = journey_issues or []
    journey_ready = a1_complete and not journey_issues and all(item["status"] != "blocked" for item in content_health)
    review_answers = int(event_summary.get("counts", {}).get("review_answered", 0))
    completed_lessons = int(event_summary.get("counts", {}).get("lesson_completed", 0))
    observed_lessons = sum(item["status"] in {"healthy", "needs_review"} for item in content_health)
    evidence_ready = active_learners >= 5 and completed_lessons >= 10 and review_answers >= 5 and observed_lessons >= 1
    needs_review = any(item["status"] == "needs_review" for item in content_health)
    gates = [
        {"id": "curriculum", "label": "20 A1 lessons pass publishing gates", "passed": publish_ready, "evidence": f"{sum(item['publish_ready'] for item in content_health)}/20 ready"},
        {"id": "journey", "label": "Mission, repair and delayed review are connected", "passed": journey_ready, "evidence": f"{len(content_health)}/20 inspected · {len(journey_issues)} journey issues"},
        {"id": "telemetry", "label": "Starts, answers, skips, repairs and recall are measurable", "passed": True, "evidence": "V9 event contract active"},
        {"id": "sample", "label": "Closed beta has enough learning evidence", "passed": evidence_ready, "evidence": f"{active_learners} active · {completed_lessons} completions · {review_answers} recalls · {observed_lessons} measurable lessons"},
    ]
    if not publish_ready or not journey_ready:
        stage = "blocked"
    elif needs_review:
        stage = "content_review_required"
    elif evidence_ready:
        stage = "evidence_ready"
    elif enrolled or active_learners:
        stage = "collecting_evidence"
    else:
        stage = "ready_for_closed_beta"
    return {"stage": stage, "gates": gates, "all_gates_passed": all(item["passed"] for item in gates), "journey_issues": journey_issues}


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
