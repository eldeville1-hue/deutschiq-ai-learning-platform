"""Aggregate CEFR production evidence into explainable repair priorities."""
from collections import defaultdict

DIMENSIONS = ("task_completion", "grammar", "vocabulary", "coherence", "register")
CORE_DIMENSIONS = ("task_completion", "grammar", "coherence")


def assessment_insights(attempts, minimum_samples: int = 1) -> dict:
    totals = defaultdict(float)
    counts = defaultdict(int)
    topic_totals = defaultdict(lambda: defaultdict(float))
    topic_counts = defaultdict(lambda: defaultdict(int))
    used = 0
    for attempt in attempts:
        assessment = getattr(attempt, "assessment", None) or {}
        scores = assessment.get("dimensions") or {}
        if not scores:
            continue
        used += 1
        for dimension in DIMENSIONS:
            if dimension not in scores:
                continue
            value = max(0, min(100, float(scores[dimension])))
            totals[dimension] += value
            counts[dimension] += 1
            topic_totals[str(attempt.topic)][dimension] += value
            topic_counts[str(attempt.topic)][dimension] += 1
    dimensions = {
        dimension: {"score": round(totals[dimension] / counts[dimension]), "samples": counts[dimension]}
        for dimension in DIMENSIONS if counts[dimension] >= minimum_samples
    }
    weakest = min(dimensions, key=lambda key: dimensions[key]["score"]) if dimensions else None
    topics = []
    for topic, values in topic_totals.items():
        topic_dimensions = {
            dimension: round(values[dimension] / topic_counts[topic][dimension])
            for dimension in DIMENSIONS if topic_counts[topic][dimension]
        }
        if topic_dimensions:
            weak_dimension = min(topic_dimensions, key=topic_dimensions.get)
            topics.append({"topic": topic, "dimension": weak_dimension, "score": topic_dimensions[weak_dimension], "dimensions": topic_dimensions})
    topics.sort(key=lambda item: (item["score"], item["topic"]))
    return {
        "samples": used,
        "dimensions": dimensions,
        "weakest_dimension": weakest,
        "weakest_score": dimensions.get(weakest, {}).get("score") if weakest else None,
        "priority_topics": topics[:5],
    }


def evidence_gate(attempts, required_samples: int = 3) -> dict:
    """Protect progression once enough production evidence exists; legacy users stay compatible."""
    insight = assessment_insights(attempts)
    if insight["samples"] < required_samples:
        return {"eligible": True, "status": "building_evidence", **insight}
    dimensions = insight["dimensions"]
    thresholds = {"task_completion": 60, "grammar": 55, "coherence": 50}
    gaps = [name for name in CORE_DIMENSIONS if dimensions.get(name, {}).get("score", 0) < thresholds[name]]
    return {"eligible": not gaps, "status": "ready" if not gaps else "repair_needed", "gaps": gaps, **insight}
