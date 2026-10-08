"""Reproducible *synthetic* evaluation fixture generator for DeutschIQ 88.

Generated labels are provisional and MUST NOT be described as human-reviewed.
Run: python -m tests.generate_evaluation_benchmark
"""
import json
from pathlib import Path

LEVELS = ("A1", "A2", "B1", "B2")
TEMPLATES = (
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kaffee.", "correct", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe ein Kaffee.", "incorrect", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe keinen Kaffee.", "incorrect", "choice"),
    ("Ich kaufe einen Kaffee.", "Ich hole einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich besorge einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe ein Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufen einen Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe keinen Kaffee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kafee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Tee.", "incorrect", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe einen Kaffee.", "correct", "translation"),
    ("Ich kaufe einen Kaffee.", "Ich kaufe Kaffee.", "uncertain", "translation"),
)
# Each case receives its own ID, level and contextual prompt. Repeated surface
# forms deliberately test whether the exercise objective changes the verdict.
CONTEXTS = (
    "Choose the exact response.",
    "Translate: I am buying a coffee.",
    "Translate: I am getting a coffee.",
    "Write a sentence about buying coffee.",
    "Practice accusative articles.",
    "Practice present-tense conjugation.",
    "Practice negation.",
    "Respond to a café order.",
    "Use a natural German expression.",
    "Compare the model answer with your response.",
)

def build_cases():
    rows = []
    for level in LEVELS:
        for context_index, objective in enumerate(CONTEXTS):
            for template_index, (model, response, label, kind) in enumerate(TEMPLATES):
                case_id = f"{level}-{context_index:02d}-{template_index:02d}"
                rows.append({
                    "id": case_id, "cefr": level, "objective": objective,
                    "exercise": {"type": kind, "question": objective, "answer": model},
                    "learner_answer": response,
                    "provisional_expected": label,
                    "human_review": {"status": "pending", "reviewer": None, "decision": None, "notes": ""},
                    "source": "synthetic_template",
                })
    return rows

def main():
    path = Path(__file__).resolve().parent / "fixtures" / "evaluation_v88_synthetic.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_cases()
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"Wrote {len(rows)} provisional cases to {path}")

if __name__ == "__main__":
    main()
