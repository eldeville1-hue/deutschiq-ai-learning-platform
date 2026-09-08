import ast
from pathlib import Path
import unittest

from app.services.diagnostic import calculate_level_and_scores


class BalancedPlacementTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).parents[1] / "app/api/endpoints/diagnostic.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        assignments = {
            node.targets[0].id: ast.literal_eval(node.value)
            for node in tree.body
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in {"MOCK_QUESTIONS", "PLACEMENT_QUESTION_IDS"}
        }
        self.all_questions = assignments["MOCK_QUESTIONS"]
        self.question_ids = assignments["PLACEMENT_QUESTION_IDS"]
        self.questions = [q for q in self.all_questions if q["id"] in self.question_ids]

    def test_has_four_items_per_cefr_band(self):
        counts = {level: 0 for level in ("A1", "A2", "B1", "B2")}
        for question in self.questions:
            counts[question["difficulty"]] += 1
        self.assertEqual(counts, {"A1": 4, "A2": 4, "B1": 4, "B2": 4})

    def test_has_one_listening_anchor_per_band(self):
        listening = [q for q in self.questions if q["pillar"] == "listening"]
        self.assertEqual({q["difficulty"] for q in listening}, {"A1", "A2", "B1", "B2"})
        self.assertTrue(all(q.get("audio_text") for q in listening))

    def test_perfect_balanced_test_places_at_b2(self):
        answers = {q["id"]: q["correct_answer"] for q in self.questions}
        result = calculate_level_and_scores(answers, self.all_questions)
        self.assertEqual(result["level"], "B2")
        self.assertEqual(result["pillar_attempts"]["listening"], 4)


if __name__ == "__main__":
    unittest.main()
