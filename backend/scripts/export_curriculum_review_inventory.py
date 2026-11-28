#!/usr/bin/env python3
"""Export a source-grounded editorial review inventory for the shipped A1-B2 curriculum.

This tool reports authored fields and structural indicators only. It never marks
German, translations, answer keys, or CEFR alignment as linguistically approved.
"""
import argparse
import json
import sys
from pathlib import Path

# Support direct execution from backend/scripts as used by GitHub Actions.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.content.foundation_curriculum import (
    A1_CURRICULUM, A2_CURRICULUM, build_foundation_content,
)
from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content


def _text(value):
    return value if isinstance(value, str) else ""


def _lesson(level, row, builder):
    content = builder(row)
    exercises = []
    for index, exercise in enumerate(content.get("exercises") or []):
        if not isinstance(exercise, dict):
            continue
        exercises.append({
            "index": index,
            "id": exercise.get("id"),
            "type": exercise.get("type"),
            "stage": exercise.get("stage"),
            "question": exercise.get("question"),
            "question_de": (exercise.get("i18n") or {}).get("de", {}).get("question"),
            "answer": exercise.get("answer"),
            "accepted_answers": exercise.get("accepted_answers"),
            "explanation": exercise.get("explanation"),
            "audio_text": exercise.get("audio_text"),
            "audio_url": exercise.get("audio_url"),
            "options": exercise.get("options"),
            "i18n": exercise.get("i18n"),
            "hint": exercise.get("hint"),
            "review_status": "not_independently_reviewed",
            "review_notes": [],
        })
    return {
        "level": level,
        "day": content.get("day", row[0] if isinstance(row, (tuple, list)) else None),
        "topic": content.get("topic") or (row[2] if level in ("A1", "A2") else row[2]),
        "title": content.get("title"),
        "title_de": content.get("title_de"),
        "objective": content.get("objective"),
        "communication_goal": content.get("communication_goal") or content.get("can_do"),
        "rule": content.get("rule"),
        "prerequisites": content.get("prerequisites") or [],
        "exercise_count": len(exercises),
        "stage_counts": {
            stage: sum(item["stage"] == stage for item in exercises)
            for stage in ("guided", "independent", "transfer")
        },
        "independent_productive_task": any(
            item["stage"] in ("independent", "transfer")
            and item["type"] in ("production", "dialogue", "translate", "transform", "error_repair")
            for item in exercises
        ),
        "lesson_review_status": "not_independently_reviewed",
        "review_dimensions": {
            "german_naturalness": "not_reviewed",
            "grammar_accuracy": "not_reviewed",
            "answer_key_and_variants": "not_reviewed",
            "distractor_quality": "not_reviewed",
            "ru_de_en_translation": "not_reviewed",
            "cefr_fit": "not_independently_validated",
            "feedback_quality": "not_reviewed",
        },
        "exercises": exercises,
    }


def build_inventory():
    tracks = (
        ("A1", A1_CURRICULUM, lambda row: build_foundation_content(row, "A1")),
        ("A2", A2_CURRICULUM, lambda row: build_foundation_content(row, "A2")),
        ("B1", B1_CURRICULUM, build_b1_content),
        ("B2", B2_CURRICULUM, build_b2_content),
    )
    lessons = []
    for level, rows, builder in tracks:
        lessons.extend(_lesson(level, row, builder) for row in rows)
    return {
        "schema_version": 2,
        "purpose": "editorial_review_inventory",
        "limitations": [
            "Structural indicators are not independent linguistic validation.",
            "CEFR labels are editorial claims, not certification.",
            "No lesson or exercise is marked approved by this export.",
        ],
        "summary": {
            "lesson_count": len(lessons),
            "exercise_count": sum(item["exercise_count"] for item in lessons),
            "levels": {
                level: {
                    "lessons": sum(item["level"] == level for item in lessons),
                    "exercises": sum(item["exercise_count"] for item in lessons if item["level"] == level),
                } for level in ("A1", "A2", "B1", "B2")
            },
            "not_independently_reviewed": len(lessons),
        },
        "lessons": lessons,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("curriculum-review-inventory.json"))
    args = parser.parse_args()
    inventory = build_inventory()
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(inventory["summary"], ensure_ascii=False, indent=2))
    print(f"Editorial inventory saved to {args.output}")


if __name__ == "__main__":
    main()
