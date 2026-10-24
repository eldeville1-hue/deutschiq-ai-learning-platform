import unittest
from app.services.tutor_clause_bank import CLAUSE_DRILLS
from app.services.tutor_verified_practice import grade_reviewed_word_order, verified_specific_feedback


class ClauseErrorDetectionTests(unittest.TestCase):
    def test_missing_comma_is_detected_for_reviewed_clauses(self):
        for identifier, _level, topic, expected, words, variants in CLAUSE_DRILLS:
            for answer in (expected, *variants):
                if answer.count(",") != 1:
                    continue
                with self.subTest(identifier=identifier, answer=answer):
                    result = grade_reviewed_word_order("Exercise: " + words, answer.replace(",", ""))
                    self.assertIs(result["correct"], False)
                    self.assertEqual(result["reason"], "missing_clause_comma")
                    self.assertEqual(result["topic"], topic)

    def test_other_changes_remain_unverified(self):
        result = grade_reviewed_word_order(
            "Exercise: obwohl ich müde bin / lerne ich weiter",
            "Obwohl ich krank bin lerne ich weiter.",
        )
        self.assertIsNone(result["correct"])

    def test_localized_comma_feedback(self):
        for lang, phrase in (("ru", "запятая"), ("de", "Komma"), ("en", "comma")):
            with self.subTest(lang=lang):
                self.assertIn(phrase, verified_specific_feedback("weil_clause", "missing_clause_comma", lang))

    def test_unrelated_reason_uses_existing_hint(self):
        feedback = verified_specific_feedback("konjunktiv_ii", "", "de")
        self.assertIn("hypothetische", feedback)


if __name__ == "__main__":
    unittest.main()
