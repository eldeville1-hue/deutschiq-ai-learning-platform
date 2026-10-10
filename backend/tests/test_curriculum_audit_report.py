import unittest
from unittest.mock import patch

import seed_30_day_plan


class CurriculumAuditTests(unittest.TestCase):
    def test_clean_curriculum_has_no_issues(self):
        report = seed_30_day_plan.curriculum_audit_report()
        self.assertEqual({"30-day roadmap", "A1", "A2", "B1", "B2"}, set(report))
        self.assertTrue(all(not failures for failures in report.values()))

    def test_reports_multiple_late_failures_without_database_writes(self):
        original = seed_30_day_plan.build_b2_content

        def broken_b2(row):
            result = original(row)
            if row[0] in {seed_30_day_plan.B2_CURRICULUM[-1][0], seed_30_day_plan.B2_CURRICULUM[-2][0]}:
                result["objective"] = ""
            return result

        with patch.object(seed_30_day_plan, "build_b2_content", side_effect=broken_b2):
            report = seed_30_day_plan.curriculum_audit_report()
            self.assertEqual(2, len(report["B2"]))
            self.assertTrue(all("missing:objective" in item["issues"] for item in report["B2"]))
            with patch.object(seed_30_day_plan, "SessionLocal") as session:
                with self.assertRaisesRegex(ValueError, "Refusing to publish curriculum"):
                    seed_30_day_plan.seed()
                session.assert_not_called()


if __name__ == "__main__":
    unittest.main()
