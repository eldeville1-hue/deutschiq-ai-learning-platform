from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class V9LearningProofTests(unittest.TestCase):
    def test_frontend_learning_events_are_accepted_by_backend(self):
        events = (ROOT / "backend/app/api/endpoints/events.py").read_text(encoding="utf-8")
        lesson = (ROOT / "frontend/mini-app/src/pages/Lesson.tsx").read_text(encoding="utf-8")
        review = (ROOT / "frontend/mini-app/src/pages/Review.tsx").read_text(encoding="utf-8")
        for name in ("exercise_skipped", "mission_repair_completed", "review_answered"):
            self.assertIn(f'"{name}"', events)
            self.assertIn(f"'{name}'", lesson + review)

    def test_owner_center_exposes_readiness_and_content_health(self):
        endpoint = (ROOT / "backend/app/api/endpoints/internal.py").read_text(encoding="utf-8")
        page = (ROOT / "frontend/mini-app/src/pages/ControlCenter.tsx").read_text(encoding="utf-8")
        health = (ROOT / "frontend/mini-app/src/components/qa/ContentHealth.tsx").read_text(encoding="utf-8")
        self.assertIn('"content_health": content_health', endpoint)
        self.assertIn('"readiness": readiness', endpoint)
        self.assertIn('<ContentHealth data={data}', page)
        self.assertIn('Not enough evidence', health)
        self.assertIn('Rates appear only after at least five relevant observations', health)


if __name__ == "__main__":
    unittest.main()
