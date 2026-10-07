def session_score(correct_values: list[bool]) -> int:
    if not correct_values:
        return 0
    return round(sum(1 for value in correct_values if value) / len(correct_values) * 100)


def summarize_attempts(attempts) -> dict:
    """Score the latest answer per exercise and expose the value of corrected retries."""
    first = {}
    latest = {}
    for attempt in attempts:
        index = int(attempt.exercise_index)
        first.setdefault(index, bool(attempt.correct))
        latest[index] = bool(attempt.correct)
    return {
        "score": session_score(list(latest.values())),
        "first_try_correct": sum(1 for value in first.values() if value),
        "corrected_retries": sum(1 for index, value in latest.items() if value and not first[index]),
        "needs_review": sum(1 for value in latest.values() if not value),
        "exercise_count": len(latest),
    }


def summarize_mission(attempts, mission_index: int | None) -> dict:
    """Return evidence for the independent task that closes a mission lesson.

    A supported word-tile retry may repair an earlier error, but it is not
    independent production.  Therefore a mission is demonstrated only by a
    successful production assessment on the designated final exercise.
    """
    if mission_index is None:
        return {
            "mission_required": False,
            "mission_attempted": False,
            "mission_passed": True,
            "mission_score": None,
            "mission_answer": None,
        }

    mission_attempts = [
        attempt for attempt in attempts
        if int(attempt.exercise_index) == int(mission_index)
        and getattr(attempt, "production_score", None) is not None
    ]
    latest = mission_attempts[-1] if mission_attempts else None
    score = int(latest.production_score) if latest and latest.production_score is not None else None
    return {
        "mission_required": True,
        "mission_attempted": latest is not None,
        "mission_passed": bool(latest and latest.correct and score is not None and score >= 70),
        "mission_score": score,
        "mission_answer": latest.answer if latest else None,
    }


def mastery_update(
    current: float,
    correct: bool,
    confidence: str | None,
    response_ms: int | None = None,
) -> float:
    """Update mastery without confusing confidence with demonstrated recall."""
    confidence_weight = 1.08 if confidence == "sure" else .82 if confidence == "guess" else 1.0
    speed_weight = 1.0
    if response_ms and response_ms > 0:
        speed_weight = .88 if response_ms > 45_000 else 1.04 if response_ms < 8_000 else 1.0
    # A confident error is a stronger misconception signal than a guessed error.
    if not correct and confidence == "sure":
        confidence_weight = 1.18
    delta = (12 if correct else -11) * confidence_weight * speed_weight
    return max(0.0, min(100.0, current + delta))


def mastery_update_from_evidence(
    current: float,
    score: int,
    confidence: str | None,
    response_ms: int | None = None,
) -> float:
    """Use rubric evidence for open production instead of reducing it to a binary answer."""
    bounded = max(0, min(100, int(score)))
    correct = bounded >= 70
    binary_target = mastery_update(current, correct, confidence, response_ms)
    evidence_target = current + ((bounded - 60) / 5 if correct else -((70 - bounded) / 4 + 4))
    return max(0.0, min(100.0, binary_target * .45 + evidence_target * .55))


def review_interval(correct: bool, streak: int) -> int:
    if not correct:
        return 1
    intervals = [1, 3, 7, 14, 30]
    return intervals[min(max(streak - 1, 0), len(intervals) - 1)]


def retrieval_review_interval(correct: bool, stability_days: float) -> int:
    """Schedule from independent retrieval stability, never lesson-card streaks."""
    if not correct:
        return 1
    return max(3, min(30, round(max(1.0, stability_days))))


def retention_score(mastery: float, stability_days: float, days_overdue: float = 0.0) -> int:
    """A conservative, explainable estimate used for prioritisation, not a CEFR score."""
    decay = max(0.0, days_overdue) * (7.0 / max(1.0, stability_days))
    return round(max(0.0, min(100.0, mastery - decay)))


def next_stability(current: float, correct: bool, confidence: str | None) -> float:
    if not correct:
        return max(1.0, current * .45)
    multiplier = 2.15 if confidence == "sure" else 1.55 if confidence == "guess" else 1.85
    return min(120.0, max(1.0, current) * multiplier)


def adaptive_mastery_update(
    current: float,
    correct: bool,
    confidence: str | None,
    response_ms: int | None = None,
    *,
    retry: bool = False,
    retrieval: bool = False,
    production_score: int | None = None,
) -> float:
    """Update mastery according to evidence independence.

    Supported retries prove repair, not durable recall, so positive gains are
    deliberately smaller. Independent delayed retrieval is stronger evidence
    and earns a modest boost. Errors are never softened by retry/review mode.
    """
    if production_score is not None:
        target = mastery_update_from_evidence(current, production_score, confidence, response_ms)
    else:
        target = mastery_update(current, correct, confidence, response_ms)
    delta = target - current
    if delta <= 0:
        return target
    evidence_weight = 0.45 if retry else (1.20 if retrieval else 1.0)
    return max(0.0, min(100.0, current + delta * evidence_weight))


def adaptive_priority_score(mastery: float, stability_days: float, days_overdue: float = 0.0) -> int:
    """Expose the decayed skill strength used when choosing what to learn next."""
    return retention_score(mastery, stability_days, days_overdue)
