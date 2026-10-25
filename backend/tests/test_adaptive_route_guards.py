"""Guard personalized lesson routing against stale errors and locked content."""
import unittest
from types import SimpleNamespace

from app.services.learning_route import select_recommended_lesson, filter_roadmap_for_level
from app.services.lesson_coaching import repeated_error_focus


def lesson(identifier, topic, day, prerequisites=None):
    return SimpleNamespace(
        id=identifier,
        topic=topic,
        content={"track": "A2", "day": day, "prerequisites": prerequisites or []},
        weak_point_tags=[topic],
    )


class AdaptiveRouteGuardTests(unittest.TestCase):
    def setUp(self):
        self.intro = lesson(1, "word_order", 1)
        self.articles = lesson(2, "articles", 2)
        self.advanced = lesson(3, "relative_clauses", 3, ["articles"])
        self.lessons = [self.intro, self.articles, self.advanced]

    def test_inactive_duplicate_is_not_recommended_even_when_focused(self):
        duplicate = lesson(99, "articles", 2)
        duplicate.is_active = False
        self.articles.is_active = True
        selected = select_recommended_lesson(
            [duplicate, self.articles], set(), {}, {},
            focus_skill="articles",
        )
        self.assertEqual(selected.id, self.articles.id)

    def test_inactive_lessons_are_excluded_from_fallback_route(self):
        inactive = lesson(99, "word_order", 1)
        inactive.content["track"] = "foundation"
        inactive.is_active = False
        active = lesson(100, "articles", 2)
        active.content["track"] = "foundation"
        active.is_active = True
        self.assertEqual(filter_roadmap_for_level([inactive, active], "B2"), [active])

    def test_repeated_errors_select_available_skill(self):
        history = [{"skill_id": "articles", "correct": False}] * 2
        focus = repeated_error_focus(history, {item.topic for item in self.lessons})
        selected = select_recommended_lesson(
            self.lessons, set(), {"word_order": 85}, {}, focus_skill=focus
        )
        self.assertEqual(selected.id, self.articles.id)

    def test_completed_lesson_is_not_recommended_for_old_errors(self):
        selected = select_recommended_lesson(
            self.lessons, {self.articles.id}, {}, {}, focus_skill="articles"
        )
        self.assertNotEqual(selected.id, self.articles.id)

    def test_repeated_errors_do_not_unlock_prerequisite(self):
        selected = select_recommended_lesson(
            self.lessons, set(), {}, {}, focus_skill="relative_clauses"
        )
        self.assertNotEqual(selected.id, self.advanced.id)

    def test_recovery_restores_normal_route(self):
        history = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": True},
            {"skill_id": "articles", "correct": True},
        ]
        focus = repeated_error_focus(history, {item.topic for item in self.lessons})
        self.assertIsNone(focus)
        selected = select_recommended_lesson(
            self.lessons, set(), {}, {}, focus_skill=focus
        )
        self.assertEqual(selected.id, self.intro.id)


if __name__ == "__main__":
    unittest.main()
