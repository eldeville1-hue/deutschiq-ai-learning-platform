def session_score(correct_values: list[bool]) -> int:
    if not correct_values:
        return 0
    return round(sum(1 for value in correct_values if value) / len(correct_values) * 100)


def mastery_update(current: float, correct: bool, confidence: str | None) -> float:
    weight = 1.1 if confidence == "sure" else .85 if confidence == "guess" else 1.0
    delta = (14 if correct else -10) * weight
    return max(0.0, min(100.0, current + delta))


def review_interval(correct: bool, streak: int) -> int:
    if not correct:
        return 1
    intervals = [1, 3, 7, 14, 30]
    return intervals[min(max(streak - 1, 0), len(intervals) - 1)]
