import unittest

from app.content.b2_curriculum import B2_CURRICULUM, build_b2_content
from app.services.content_quality import exercise_instruction_audit, exercise_answer_audit


class B2CurriculumEditorialAuditTests(unittest.TestCase):
    def test_every_b2_lesson_has_usable_instructions_and_listening_source(self):
        problems = {}
        for row in B2_CURRICULUM:
            content = build_b2_content(row)
            issues = exercise_instruction_audit(content)
            if issues:
                problems[row[2]] = issues
        self.assertEqual({}, problems)

    def test_every_b2_lesson_has_usable_objective_answers(self):
        problems = {}
        for row in B2_CURRICULUM:
            content = build_b2_content(row)
            issues = exercise_answer_audit(content)
            if issues:
                problems[row[2]] = issues
        self.assertEqual({}, problems)


if __name__ == "__main__":
    unittest.main()
