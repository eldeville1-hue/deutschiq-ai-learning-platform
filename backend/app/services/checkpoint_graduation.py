"""Pure graduation-checkpoint rules, shared by the API and regression tests."""

from app.services.production_feedback import DIMENSIONS


def final_mission(content: dict) -> dict:
    return next((
        item for item in content.get("exercises", [])
        if item.get("mission_role") == "final" and item.get("type") in {"production", "dialogue"}
    ), {})


def checkpoint_outcome(results: list[dict]) -> dict:
    score = round(sum(item["score"] for item in results) / max(len(results), 1))
    dimension_scores = {
        name: round(sum(item["dimensions"].get(name, 0) for item in results) / max(len(results), 1))
        for name in DIMENSIONS
    }
    passed = bool(results) and score >= 70 and dimension_scores["task_completion"] >= 65 and dimension_scores["grammar"] >= 55
    return {"score": score, "dimensions": dimension_scores, "passed": passed}
