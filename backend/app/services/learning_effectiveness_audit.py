"""Editorial indicators of lesson practice, not evidence of learning outcomes."""


def learning_effectiveness_evidence(content: dict) -> dict:
    exercises = [item for item in content.get("exercises", []) if isinstance(item, dict)]
    counts = {stage: sum(item.get("stage") == stage for item in exercises)
              for stage in ("guided", "independent", "transfer")}
    productive = {"production", "dialogue", "translate", "transform", "error_repair"}
    independent_production = any(
        item.get("stage") in {"independent", "transfer"} and item.get("type") in productive
        for item in exercises
    )
    issues = [f"effectiveness:missing_{stage}_practice"
              for stage, count in counts.items() if not count]
    if not independent_production:
        issues.append("effectiveness:no_independent_productive_task")
    if not content.get("communication_goal") and not content.get("can_do"):
        issues.append("effectiveness:missing_communicative_outcome")
    return {
        "stage_counts": counts,
        "independent_productive_task": independent_production,
        "issues": issues,
    }
