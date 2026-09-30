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

    def test_empty_checkpoint_never_passes(self):
        self.assertFalse(checkpoint_outcome([])["passed"])


if __name__ == "__main__":
    unittest.main()
