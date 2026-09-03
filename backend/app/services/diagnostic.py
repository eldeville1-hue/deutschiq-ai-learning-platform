# backend/app/services/diagnostic.py
from typing import Dict, List

LEVEL_THRESHOLDS = {'A1': 0.4, 'A2': 0.55, 'B1': 0.7, 'B2': 0.85, 'C1': 0.95}

def calculate_level_and_scores(answers: Dict[int, str], questions: List[dict]) -> dict:
    total = len(answers)
    correct = 0
    pillar_correct = {'grammar': 0, 'vocabulary': 0, 'listening': 0, 'pronunciation': 0}
    pillar_total = {'grammar': 0, 'vocabulary': 0, 'listening': 0, 'pronunciation': 0}
    weak_points = {}

    for q in questions:
        q_id = q['id']
        pillar = q.get('pillar', 'grammar')
        pillar_total[pillar] += 1
        if answers.get(q_id) == q['correct_answer']:
            correct += 1
            pillar_correct[pillar] += 1
        else:
            for tag in q.get('weak_tags', []):
                weak_points[tag] = weak_points.get(tag, 0) + 1

    overall_pct = (correct / total) * 100 if total > 0 else 0
    level = 'A1'
    for lvl, threshold in LEVEL_THRESHOLDS.items():
        if overall_pct / 100 >= threshold:
            level = lvl

    pillar_scores = {}
    for p in pillar_total:
        t = pillar_total[p]
        pillar_scores[p] = round((pillar_correct[p] / t) * 10, 1) if t > 0 else 0

    return {
        "level": level,
        "overall_score": round(overall_pct, 1),
        "pillars": pillar_scores,
        "weak_points": weak_points
    }

