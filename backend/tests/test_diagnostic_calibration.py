import unittest

from app.services.diagnostic import calculate_level_and_scores

QUESTIONS = []
question_id = 1
for difficulty, count in (("A1", 4), ("A2", 5), ("B1", 5), ("B2", 4), ("C1", 2)):
    for _ in range(count):
        QUESTIONS.append({
            "id": question_id,
            "pillar": "grammar",
            "difficulty": difficulty,
            "correct_answer": f"answer-{question_id}",
            "weak_tags": [f"topic-{question_id}"],
        })
        question_id += 1


class DiagnosticCalibrationTests(unittest.TestCase):
    def answers_through(self, last_id: int) -> dict[int, str]:
        return {
            question["id"]: question["correct_answer"]
            for question in QUESTIONS
            if question["id"] <= last_id
        }

    def test_perfect_legacy_fifteen_question_test_caps_at_b1(self):
        result = calculate_level_and_scores(self.answers_through(15), QUESTIONS)
        self.assertEqual(result["overall_score"], 100)
        self.assertEqual(result["level"], "B1")
        self.assertEqual(result["assessment_ceiling"], "B1")

    def test_b2_requires_enough_b1_evidence(self):
        result = calculate_level_and_scores(self.answers_through(18), QUESTIONS)
        self.assertEqual(result["level"], "B2")
        self.assertEqual(result["assessment_ceiling"], "B2")

    def test_missing_answers_do_not_inflate_score(self):
        result = calculate_level_and_scores({1: "answer-1"}, QUESTIONS)
        self.assertEqual(result["overall_score"], 100)
        self.assertEqual(result["level"], "A1")

    def test_wrong_higher_band_cannot_be_hidden_by_easy_items(self):
        answers = self.answers_through(14)
        for question_id in range(10, 15):
            answers[question_id] = "wrong"
        result = calculate_level_and_scores(answers, QUESTIONS)
        self.assertEqual(result["level"], "A2")


if __name__ == "__main__":
    unittest.main()
