"""Check the actual shipped A1–B2 exercises, not only synthetic fixtures."""
import unittest

from app.content.foundation_curriculum import A1_CURRICULUM, A2_CURRICULUM, build_foundation_content
from app.content.b1_curriculum import B1_CURRICULUM, build_b1_content
from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content
from app.services.content_quality import exercise_answer_audit
from app.services.content_i18n import localize_lesson_content


class PublishedCurriculumChoiceAuditTests(unittest.TestCase):
    def test_shipped_choice_questions_have_usable_distractors_in_each_language(self):
        curriculum = (
            [("A1", row, build_foundation_content(row, "A1")) for row in A1_CURRICULUM]
            + [("A2", row, build_foundation_content(row, "A2")) for row in A2_CURRICULUM]
            + [("B1", row, build_b1_content(row)) for row in B1_CURRICULUM]
            + [("B2", row, build_b2_content(row)) for row in B2_CURRICULUM]
        )
        defects = []
        for level, row, content in curriculum:
            for language in ("ru", "de", "en"):
                localized = localize_lesson_content(content, language)
                for issue in exercise_answer_audit(localized):
                    if issue.endswith(("invalid_options", "duplicate_options", "answer_not_in_options", "no_incorrect_distractor")):
                        defects.append(f"{level}/{row[2]}/{language}: {issue}")
        self.assertEqual(defects, [], "Fix these shipped lesson choice tasks:\\n" + "\\n".join(defects))


if __name__ == "__main__":
    unittest.main()
