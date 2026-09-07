def session_score(correct_values: list[bool]) -> int:
    if not correct_values:
        return 0
    return round(sum(1 for value in correct_values if value) / len(correct_values) * 100)


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


def review_interval(correct: bool, streak: int) -> int:
    if not correct:
        return 1
    intervals = [1, 3, 7, 14, 30]
    return intervals[min(max(streak - 1, 0), len(intervals) - 1)]


def retention_score(mastery: float, stability_days: float, days_overdue: float = 0.0) -> int:
    """A conservative, explainable estimate used for prioritisation, not a CEFR score."""
    decay = max(0.0, days_overdue) * (7.0 / max(1.0, stability_days))
    return round(max(0.0, min(100.0, mastery - decay)))


def next_stability(current: float, correct: bool, confidence: str | None) -> float:
    if not correct:
        return max(1.0, current * .45)
    multiplier = 2.15 if confidence == "sure" else 1.55 if confidence == "guess" else 1.85
    return min(120.0, max(1.0, current) * multiplier)
