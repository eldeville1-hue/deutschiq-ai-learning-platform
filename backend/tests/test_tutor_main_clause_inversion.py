import unittest

from app.services.tutor_clause_bank import CLAUSE_DRILLS
from app.services.tutor_verified_practice import (
    grade_reviewed_word_order,
    verified_specific_feedback,
)


class MainClauseInversionTests(unittest.TestCase):
    def test_swapped_main_clause_start_is_detected(self):
        checked = 0
        for identifier, _level, topic, expected, chunks, alternatives in CLAUSE_DRILLS:
            for candidate in (expected, *alternatives):
                if candidate.count(",") != 1:
                    continue
                first, second = [part.strip() for part in candidate.rstrip(".").split(",")]
                if not first.casefold().startswith(("weil ", "obwohl ", "damit ", "wenn ")):
                    continue
                tokens = second.split()
                if len(tokens) < 3:
                    continue
                malformed = candidate.replace(second, " ".join((tokens[1], tokens[0], *tokens[2:])))
                with self.subTest(identifier=identifier, candidate=candidate):
                    result = grade_reviewed_word_order("Exercise: " + chunks, malformed)
                    self.assertIs(result["correct"], False)
                    self.assertEqual(result["reason"], "main_clause_inversion")
                    checked += 1
        self.assertGreaterEqual(checked, 4)

    def test_reviewed_correct_sentences_still_pass(self):
        for identifier, _level, topic, expected, chunks, alternatives in CLAUSE_DRILLS:
            for answer in (expected, *alternatives):
                with self.subTest(identifier=identifier):
                    self.assertIs(
                        grade_reviewed_word_order("Exercise: " + chunks, answer)["correct"],
                        True,
                    )

    def test_unreviewed_answer_remains_uncertain(self):
        result = grade_reviewed_word_order(
            "Exercise: obwohl ich müde bin / lerne ich weiter",
            "Obwohl ich sehr müde bin, lerne ich weiter.",
        )
        self.assertIsNone(result["correct"])

    def test_localized_feedback(self):
        for lang, fragment in (("ru", "глагола"), ("de", "Verb"), ("en", "verb")):
            self.assertIn(fragment, verified_specific_feedback("weil_clause", "main_clause_inversion", lang))


if __name__ == "__main__":
    unittest.main()
