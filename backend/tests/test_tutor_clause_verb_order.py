import unittest

from app.services.tutor_clause_bank import CLAUSE_DRILLS
from app.services.tutor_verified_practice import (
    grade_reviewed_word_order,
    verified_specific_feedback,
)


class ClauseVerbOrderTests(unittest.TestCase):
    def test_exact_verb_second_error_in_subordinate_clause(self):
        for identifier, _level, topic, expected, chunks, alternatives in CLAUSE_DRILLS:
            if topic not in ("weil_clause", "obwohl_clause", "damit_clause"):
                continue
            for candidate in (expected, *alternatives):
                parts = [part.strip() for part in candidate.rstrip(".").split(",")]
                subordinate = next(
                    (part for part in parts if part.casefold().startswith(("weil ", "obwohl ", "damit "))),
                    None,
                )
                if not subordinate:
                    continue
                tokens = subordinate.split()
                if len(tokens) < 4:
                    continue
                malformed = candidate.replace(subordinate, " ".join((tokens[0], tokens[-1], *tokens[1:-1])))
                with self.subTest(identifier=identifier, candidate=candidate):
                    result = grade_reviewed_word_order("Exercise: " + chunks, malformed)
                    self.assertIs(result["correct"], False)
                    self.assertEqual(result["reason"], "subordinate_verb_position")

    def test_correct_answers_remain_correct(self):
        for identifier, _level, topic, expected, chunks, alternatives in CLAUSE_DRILLS:
            for answer in (expected, *alternatives):
                with self.subTest(identifier=identifier):
                    result = grade_reviewed_word_order("Exercise: " + chunks, answer)
                    self.assertIs(result["correct"], True)

    def test_unreviewed_change_is_not_declared_wrong(self):
        result = grade_reviewed_word_order(
            "Exercise: obwohl ich müde bin / lerne ich weiter",
            "Obwohl ich heute müde bin, lerne ich weiter.",
        )
        self.assertIsNone(result["correct"])

    def test_localized_verb_position_feedback(self):
        for lang, fragment in (("ru", "глагол"), ("de", "Verb"), ("en", "verb")):
            self.assertIn(fragment, verified_specific_feedback("weil_clause", "subordinate_verb_position", lang))


if __name__ == "__main__":
    unittest.main()
