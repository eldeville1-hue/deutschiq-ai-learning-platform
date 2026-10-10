import unittest
from unittest.mock import patch

import seed_30_day_plan


class CurriculumPreflightTests(unittest.TestCase):
    def test_valid_curriculum_preflight(self):
        seed_30_day_plan.validate_all_curriculum_before_seed()

    def test_invalid_later_track_blocks_before_database_session(self):
        original = seed_30_day_plan.build_b2_content

        def invalid_b2(row):
            content = original(row)
            if row[0] == seed_30_day_plan.B2_CURRICULUM[-1][0]:
                content["exercises"][0]["answer"] = ""
                content["exercises"][0]["accepted_answers"] = []
            return content

        with patch.object(seed_30_day_plan, "build_b2_content", side_effect=invalid_b2):
            with patch.object(seed_30_day_plan, "SessionLocal") as session:
                with self.assertRaisesRegex(ValueError, "Refusing to publish B2"):
                    seed_30_day_plan.seed()
                session.assert_not_called()


if __name__ == "__main__":
    unittest.main()
