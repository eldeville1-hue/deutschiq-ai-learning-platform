import unittest

from app.services.tutor_verified_practice import grade_reviewed_word_order, verified_retry_feedback


class ReviewedWordOrderTests(unittest.TestCase):
    def test_topic_hints_are_localized_and_do_not_diagnose_error(self):
        for lang in ("ru", "de", "en"):
            feedback = verified_retry_feedback("dative_case", lang)
            self.assertTrue(feedback)
            self.assertNotIn("word order", feedback.casefold())
        self.assertIn("Dativ", verified_retry_feedback("dative_case", "de"))
        self.assertIn("sein", verified_retry_feedback("perfekt_auxiliary", "en"))

    def test_exact_answer_is_verified(self):
        result = grade_reviewed_word_order(
            "Exercise: Put these words in order: “heute / ich / Deutsch / lerne”.",
            "Heute lerne ich Deutsch.",
        )
        self.assertIsNotNone(result)
        self.assertTrue(result["correct"])
        self.assertEqual(result["topic"], "word_order")

    def test_case_and_final_punctuation_do_not_change_result(self):
        result = grade_reviewed_word_order(
            "Übung: Ordne „ich / helfe / dem Mann“.",
            "ich helfe dem mann!",
        )
        self.assertTrue(result["correct"])

    def test_reviewed_alternative_word_order_is_accepted(self):
        result = grade_reviewed_word_order(
            "Exercise: heute / ich / Deutsch / lerne",
            "Ich lerne heute Deutsch.",
        )
        self.assertTrue(result["correct"])

    def test_reviewed_genitive_alternative_is_accepted(self):
        result = grade_reviewed_word_order(
            "Übung: wegen / des Regens / bleiben wir zu Hause",
            "Wir bleiben wegen des Regens zu Hause.",
        )
        self.assertTrue(result["correct"])

    def test_unreviewed_reordering_is_not_assumed_correct(self):
        result = grade_reviewed_word_order(
            "Exercise: ich / helfe / dem Mann",
            "Dem Mann helfe ich.",
        )
        self.assertIsNone(result["correct"])

    def test_wrong_answer_does_not_claim_success(self):
        result = grade_reviewed_word_order(
            "Exercise: Put these words in order: “heute / ich / Deutsch / lerne”.",
            "Ich heute lerne Deutsch.",
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["reason"], "verb_position")

    def test_unreviewed_haben_variant_is_not_called_wrong(self):
        result = grade_reviewed_word_order(
            "Exercise: du / hast / heute Zeit", "Zeit hast du heute."
        )
        self.assertIsNone(result["correct"])

    def test_confident_haben_v2_error(self):
        result = grade_reviewed_word_order(
            "Exercise: du / hast / heute Zeit", "Du heute hast Zeit."
        )
        self.assertFalse(result["correct"])
        self.assertEqual(result["reason"], "verb_position")

    def test_unreviewed_or_ambiguous_tasks_not_graded(self):
        self.assertIsNone(grade_reviewed_word_order("Exercise: translate this poem.", "Hallo"))
        self.assertIsNone(grade_reviewed_word_order(
            "Exercise: heute / ich / Deutsch / lerne and ich / helfe / dem Mann",
            "Heute lerne ich Deutsch.",
        ))

    def test_questions_and_empty_attempts_not_graded(self):
        self.assertIsNone(grade_reviewed_word_order(
            "Exercise: heute / ich / Deutsch / lerne", "Can you explain?"
        ))
        self.assertIsNone(grade_reviewed_word_order(
            "Exercise: heute / ich / Deutsch / lerne", "  "
        ))


if __name__ == "__main__":
    unittest.main()
