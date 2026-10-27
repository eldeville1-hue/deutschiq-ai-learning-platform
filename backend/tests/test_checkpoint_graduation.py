import unittest

from app.services.checkpoint_graduation import checkpoint_outcome, final_mission
from app.services.production_feedback import DIMENSIONS


def result(score: int, **overrides) -> dict:
    dimensions = {name: score for name in DIMENSIONS}
    dimensions.update(overrides)
    return {"score": score, "dimensions": dimensions}


class CheckpointGraduationTests(unittest.TestCase):
    def test_designated_final_mission_is_selected(self):
        content = {"exercises": [
            {"type": "dialogue", "question": "practice"},
            {"type": "dialogue", "mission_role": "final", "question": "graduation"},
        ]}
        self.assertEqual("graduation", final_mission(content)["question"])

    def test_clear_independent_performance_unlocks_next_level(self):
        outcome = checkpoint_outcome([result(78), result(74), result(82), result(76)])
        self.assertTrue(outcome["passed"])
        self.assertEqual(78, outcome["score"])

    def test_weak_grammar_blocks_promotion_even_with_high_average(self):
        outcome = checkpoint_outcome([
            result(82, grammar=45), result(82, grammar=50),
            result(82, grammar=52), result(82, grammar=54),
        ])
        self.assertFalse(outcome["passed"])
        self.assertLess(outcome["dimensions"]["grammar"], 55)

    def test_many_high_scores_cannot_hide_a_weak_grammar_dimension(self):
        outcome = checkpoint_outcome([
            result(95, grammar=40),
            result(95, grammar=45),
            result(95, grammar=50),
            result(95, grammar=52),
        ])
        self.assertFalse(outcome["passed"])
        self.assertGreater(outcome["score"], 90)

    def test_low_task_completion_blocks_high_overall_score(self):
        outcome = checkpoint_outcome([
            result(90, task_completion=55),
            result(90, task_completion=60),
            result(90, task_completion=62),
        ])
        self.assertFalse(outcome["passed"])
        self.assertLess(outcome["dimensions"]["task_completion"], 65)

    def test_high_average_with_insufficient_grammar_does_not_pass(self):
        outcome = checkpoint_outcome([
            result(90, grammar=53),
            result(90, grammar=54),
            result(90, grammar=54),
        ])
        self.assertFalse(outcome["passed"])

    def test_empty_checkpoint_never_passes(self):
        self.assertFalse(checkpoint_outcome([])["passed"])


if __name__ == "__main__":
    unittest.main()
