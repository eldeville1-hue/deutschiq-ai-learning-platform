from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class OwnerQaTests(unittest.TestCase):
    def test_qa_lab_covers_required_mobile_matrix(self):
        source = (ROOT / "frontend/mini-app/src/components/qa/QaPreviewLab.tsx").read_text(encoding="utf-8")
        for width in (320, 360, 390, 430):
            self.assertIn(str(width), source)
        for state in ("loading", "offline", "error", "wrong", "retry", "complete", "pass", "fail", "mic_denied"):
            self.assertIn(f"'{state}'", source)
        for surface in ("overview", "plan", "lesson", "checkpoint", "promotion"):
            self.assertIn(f"'{surface}'", source)
        self.assertIn('<option value="ru">RU</option>', source)
        self.assertIn('<option value="de">DE</option>', source)
        self.assertNotIn('<option value="en">EN</option>', source)

    def test_qa_preview_has_no_learner_write_calls(self):
        source = (ROOT / "frontend/mini-app/src/components/qa/QaPreviewLab.tsx").read_text(encoding="utf-8")
        allowed_read = "api.getCurriculumPreviewLesson"
        api_calls = [line.strip() for line in source.splitlines() if "api." in line]
        self.assertEqual([line for line in api_calls if allowed_read not in line], [])

    def test_control_center_requires_backend_verified_key_before_qa_mounts(self):
        source = (ROOT / "frontend/mini-app/src/pages/ControlCenter.tsx").read_text(encoding="utf-8")
        internal = (ROOT / "backend/app/api/endpoints/internal.py").read_text(encoding="utf-8")
        self.assertIn("if (!data) return", source)
        self.assertIn("<QaPreviewLab accessKey={key}", source)
        self.assertIn("compare_digest(x_control_key, settings.TASK_SECRET)", internal)


if __name__ == "__main__":
    unittest.main()
