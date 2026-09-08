# backend/app/services/diagnostic.py
from typing import Dict, List

LEVEL_ORDER = ("A1", "A2", "B1", "B2", "C1")
PROMOTION_RULES = {
    "A2": ("A2", .60, 4),
    "B1": ("B1", .60, 4),
    "B2": ("B2", .75, 4),
}

def calculate_level_and_scores(answers: Dict[int, str], questions: List[dict]) -> dict:
    answered_questions = [question for question in questions if question['id'] in answers]
    total = len(answered_questions)
    correct = 0
    pillar_correct = {'grammar': 0, 'vocabulary': 0, 'listening': 0, 'pronunciation': 0}
    pillar_total = {'grammar': 0, 'vocabulary': 0, 'listening': 0, 'pronunciation': 0}
    weak_points = {}
    level_correct = {level: 0 for level in LEVEL_ORDER}
    level_total = {level: 0 for level in LEVEL_ORDER}

    for q in questions:
        q_id = q['id']
        pillar = q.get('pillar', 'grammar')
        if q_id not in answers:
            continue
        pillar_total[pillar] += 1
        difficulty = q.get('difficulty', 'A1')
        level_total[difficulty] = level_total.get(difficulty, 0) + 1
        if answers.get(q_id) == q['correct_answer']:
            correct += 1
            pillar_correct[pillar] += 1
            level_correct[difficulty] = level_correct.get(difficulty, 0) + 1
        else:
            for tag in q.get('weak_tags', []):
                weak_points[tag] = weak_points.get(tag, 0) + 1

    overall_pct = (correct / total) * 100 if total > 0 else 0
    # A CEFR level requires evidence in the preceding difficulty band. A high
    # aggregate score can no longer skip a band or infer C1 from A1–B1 items.
    level = 'A1'
    for promoted_level in ("A2", "B1", "B2"):
        band, required_accuracy, required_answers = PROMOTION_RULES[promoted_level]
        attempts = level_total.get(band, 0)
        accuracy = level_correct.get(band, 0) / attempts if attempts else 0
        if attempts < required_answers or accuracy < required_accuracy:
            break
        level = promoted_level

    pillar_scores = {}
    for p in pillar_total:
        t = pillar_total[p]
        pillar_scores[p] = round((pillar_correct[p] / t) * 10, 1) if t > 0 else 0

    level_scores = {
        band: round(level_correct.get(band, 0) / attempts * 100)
        for band, attempts in level_total.items() if attempts
    }
    return {
        "level": level,
        "overall_score": round(overall_pct, 1),
        "pillars": pillar_scores,
        "weak_points": weak_points,
        "level_scores": level_scores,
        "pillar_attempts": pillar_total,
        "assessment_ceiling": "B1" if level_total.get("B2", 0) < 4 else "B2",
    }
