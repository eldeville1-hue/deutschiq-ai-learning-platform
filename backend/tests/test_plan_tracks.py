import unittest
from types import SimpleNamespace

from app.api.endpoints import plan as plan_endpoints
from app.models.lesson import Lesson
from app.services.learning_route import curriculum_track_for_level, filter_roadmap_for_level, next_cefr_track, normalize_cefr, track_access


def lesson(day, track=None):
    content = {"day": day}
    if track:
        content["track"] = track
    return SimpleNamespace(content=content)


class PlanTrackTests(unittest.TestCase):
    def test_journey_endpoint_has_the_lesson_model_available(self):
        self.assertIs(Lesson, plan_endpoints.Lesson)

    def test_levels_map_to_expected_track(self):
        self.assertEqual("A1", curriculum_track_for_level("A1"))
        self.assertEqual("A2", curriculum_track_for_level("A2"))
        self.assertEqual("B1", curriculum_track_for_level("B1"))
        self.assertEqual("B2", curriculum_track_for_level("B2"))
        self.assertEqual("B2", curriculum_track_for_level("C1"))
        self.assertEqual("A1", curriculum_track_for_level("A1+"))
        self.assertEqual("B1", curriculum_track_for_level("b1+"))

    def test_b1_route_is_selected_without_mixing_foundation_days(self):
        lessons = [lesson(1), lesson(31, "B1"), lesson(2), lesson(32, "B1")]
        selected = filter_roadmap_for_level(lessons, "B1")
        self.assertEqual([31, 32], [item.content["day"] for item in selected])

    def test_a1_and_a2_routes_do_not_mix(self):
        lessons = [lesson(1, "A1"), lesson(1, "A2"), lesson(2, "A1"), lesson(2, "A2")]
        self.assertEqual([1, 2], [item.content["day"] for item in filter_roadmap_for_level(lessons, "A1")])
        self.assertTrue(all(item.content["track"] == "A2" for item in filter_roadmap_for_level(lessons, "A2")))

    def test_missing_b1_route_falls_back_to_a2(self):
        selected = filter_roadmap_for_level([lesson(1), lesson(1, "A2"), lesson(2, "A2")], "B1")
        self.assertEqual([1, 2], [item.content["day"] for item in selected])

    def test_b2_route_is_selected_without_mixing_b1(self):
        lessons = [lesson(31, "B1"), lesson(55, "B2"), lesson(56, "B2")]
        selected = filter_roadmap_for_level(lessons, "B2")
        self.assertEqual([55, 56], [item.content["day"] for item in selected])

    def test_journey_access_keeps_lower_levels_open_and_higher_levels_locked(self):
        self.assertEqual("review", track_access("A1", "B1"))
        self.assertEqual("active", track_access("B1", "B1+"))
        self.assertEqual("locked", track_access("B2", "B1"))
        self.assertEqual("coming_soon", track_access("C1", "B2"))
        self.assertEqual("A2", normalize_cefr("a2+"))
        self.assertEqual("A2", next_cefr_track("A1"))
        self.assertEqual("B1", next_cefr_track("A2+"))
        self.assertIsNone(next_cefr_track("B2"))


if __name__ == "__main__":
    unittest.main()
