import unittest
from types import SimpleNamespace

from app.services.learning_route import curriculum_track_for_level, filter_roadmap_for_level


def lesson(day, track=None):
    content = {"day": day}
    if track:
        content["track"] = track
    return SimpleNamespace(content=content)


class PlanTrackTests(unittest.TestCase):
    def test_levels_map_to_expected_track(self):
        self.assertEqual("foundation", curriculum_track_for_level("A1"))
        self.assertEqual("foundation", curriculum_track_for_level("A2"))
        self.assertEqual("B1", curriculum_track_for_level("B1"))
        self.assertEqual("B2", curriculum_track_for_level("B2"))
        self.assertEqual("B2", curriculum_track_for_level("C1"))

    def test_b1_route_is_selected_without_mixing_foundation_days(self):
        lessons = [lesson(1), lesson(31, "B1"), lesson(2), lesson(32, "B1")]
        selected = filter_roadmap_for_level(lessons, "B1")
        self.assertEqual([31, 32], [item.content["day"] for item in selected])

    def test_missing_b1_route_falls_back_to_foundation(self):
        selected = filter_roadmap_for_level([lesson(1), lesson(2)], "B1")
        self.assertEqual([1, 2], [item.content["day"] for item in selected])

    def test_b2_route_is_selected_without_mixing_b1(self):
        lessons = [lesson(31, "B1"), lesson(55, "B2"), lesson(56, "B2")]
        selected = filter_roadmap_for_level(lessons, "B2")
        self.assertEqual([55, 56], [item.content["day"] for item in selected])


if __name__ == "__main__":
    unittest.main()
