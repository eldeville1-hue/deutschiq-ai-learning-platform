import unittest

from app.services.answer_intelligence import evaluate_structured_answer


class CanonicalAnswerAlternativesV88Tests(unittest.TestCase):
    def test_canonical_answer_is_valid_when_alternatives_exist(self):
        exercise = {
            "type": "translation",
            "answer": "Ich gehe heute nach Hause.",
            "accepted_answers": ["Heute gehe ich nach Hause."],
        }
        for answer in ("Ich gehe heute nach Hause.", "Heute gehe ich nach Hause."):
            with self.subTest(answer=answer):
                result = evaluate_structured_answer(answer, exercise)
                self.assertTrue(result["correct"])
                self.assertEqual(result["evaluation_status"], "verified")
                self.assertEqual(result["score"], 100)

    def test_unlisted_semantic_variant_remains_uncertain(self):
        result = evaluate_structured_answer("Ich fahre heute nach Hause.", {
            "type": "translation",
            "answer": "Ich gehe heute nach Hause.",
            "accepted_answers": ["Heute gehe ich nach Hause."],
        })
        self.assertFalse(result["correct"])
        self.assertEqual(result["evaluation_status"], "uncertain")
        self.assertEqual(result["score"], 0)

    def test_blank_canonical_with_valid_alternative(self):
        result = evaluate_structured_answer("Guten Abend", {
            "type": "choice", "answer": "", "accepted_answers": ["Guten Abend"]
        })
        self.assertTrue(result["correct"])
        self.assertEqual(result["evaluation_status"], "verified")


if __name__ == "__main__":
    unittest.main()
