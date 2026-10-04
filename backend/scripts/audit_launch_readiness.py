#!/usr/bin/env python3
"""Fail CI when curriculum or production-safety invariants regress."""

from collections import Counter
from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content
from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM, build_foundation_content
from app.services.content_i18n import localize_lesson_content
from app.services.content_quality import publication_blockers, validate_roadmap_content


def lessons():
    for level, rows in (("A1", A1_CURRICULUM), ("A2", A2_CURRICULUM)):
        for row in rows:
            yield level, row[0], row[2], build_foundation_content(row, level)
    for row in B1_CURRICULUM:
        yield "B1", row[0], row[2], build_b1_content(row)
    for row in B2_CURRICULUM:
        yield "B2", row[0], row[2], build_b2_content(row)


def main() -> None:
    issues = []
    counts = Counter()
    exercise_ids = set()
    prompt_keys = set()
    for level, day, topic, content in lessons():
        counts[level] += 1
        for issue in validate_roadmap_content(content):
            issues.append(f"{level}:{day}:{topic}:{issue}")
        if int(content.get("quality_version", 0)) >= 8:
            for blocker in publication_blockers(content):
                issues.append(f"{level}:{day}:{topic}:publish:{blocker}")
        for language in ("ru", "de", "en"):
            localized = localize_lesson_content(content, language)
            for field in ("title", "objective", "rule", "scenario"):
                if not str(localized.get(field, "")).strip():
                    issues.append(f"{level}:{day}:{topic}:{language}:missing_{field}")
        for index, exercise in enumerate(content.get("exercises") or []):
            counts["exercises"] += 1
            exercise_id = exercise.get("id")
            if exercise_id:
                key = (level, exercise_id)
                if key in exercise_ids:
                    issues.append(f"{level}:{day}:{topic}:duplicate_exercise_id:{exercise_id}")
                exercise_ids.add(key)
            prompt = str(exercise.get("question", "")).strip().casefold()
            prompt_key = (level, topic, prompt)
            if prompt_key in prompt_keys:
                issues.append(f"{level}:{day}:{topic}:duplicate_prompt")
            prompt_keys.add(prompt_key)

    expected = {"A1": 20, "A2": 20, "B1": 24, "B2": 16}
    for level, target in expected.items():
        if counts[level] != target:
            issues.append(f"{level}:expected_{target}:found_{counts[level]}")
    if counts["exercises"] < 400:
        issues.append(f"curriculum:expected_at_least_400_exercises:found_{counts['exercises']}")
    if issues:
        raise SystemExit("Launch readiness audit failed:\n" + "\n".join(issues))
    print(
        "Launch readiness audit passed: "
        f"{sum(counts[level] for level in expected)} lessons, {counts['exercises']} exercises, "
        "3 UI languages, no publication blockers."
    )


if __name__ == "__main__":
    main()
