"""DeutschIQ 84: multi-day learning-intelligence regression journeys."""
import unittest
from types import SimpleNamespace

from app.services.assessment_insights import assessment_insights, evidence_gate
from app.services.lesson_coaching import repeated_error_focus
from app.services.learning_engine import adaptive_mastery_update, adaptive_priority_score, next_stability, retrieval_review_interval
from app.services.learning_route import curriculum_track_for_level, lesson_blockers, select_recommended_lesson


def lesson(lesson_id, topic, day, track, tags=None, prerequisites=None):
    return SimpleNamespace(id=lesson_id, topic=topic, content={"day": day, "track": track, "prerequisites": prerequisites or []}, weak_point_tags=tags or [topic])


def production(topic, **dimensions):
    return SimpleNamespace(topic=topic, assessment={"dimensions": dimensions})


class AdaptiveLearnerJourneyTests(unittest.TestCase):
    def test_supported_retry_does_not_fake_independent_mastery(self):
        after_error = adaptive_mastery_update(35, False, "okay")
        supported = adaptive_mastery_update(after_error, True, "sure", retry=True)
        independent = adaptive_mastery_update(after_error, True, "sure")
        self.assertGreater(supported, after_error)
        self.assertLess(supported, independent)
        self.assertLess(supported, 50)

    def test_delayed_retrieval_builds_stability_and_expands_spacing(self):
        mastery, stability = 58, 1.0
        mastery = adaptive_mastery_update(mastery, True, "sure", retrieval=True)
        stability = next_stability(stability, True, "sure")
        first_interval = retrieval_review_interval(True, stability)
        mastery = adaptive_mastery_update(mastery, True, "sure", retrieval=True)
        stability = next_stability(stability, True, "sure")
        second_interval = retrieval_review_interval(True, stability)
        self.assertGreater(mastery, 75)
        self.assertGreater(stability, 4)
        self.assertGreater(second_interval, first_interval)

    def test_forgotten_completed_skill_is_review_priority_not_relocked(self):
        word_order = lesson(1, "word_order", 1, "B1")
        connectors = lesson(2, "connectors", 2, "B1")
        route, completed = [word_order, connectors], {1}
        demonstrated = {"word_order": 82, "connectors": 74}
        retained = {"word_order": adaptive_priority_score(82, 4, 18), "connectors": adaptive_priority_score(74, 14, 0)}
        self.assertEqual([], lesson_blockers(word_order, route, completed, demonstrated))
        self.assertIs(select_recommended_lesson(route, completed, demonstrated, {}, retained), connectors)
        self.assertLess(retained["word_order"], 60)
        self.assertGreater(retained["connectors"], retained["word_order"])

    def test_recurring_b2_production_gap_becomes_targeted_repair(self):
        attempts = [
            production("argumentation", task_completion=78, grammar=48, vocabulary=86, coherence=72, register=74),
            production("argumentation", task_completion=82, grammar=52, vocabulary=88, coherence=76, register=77),
            production("formal_register", task_completion=80, grammar=68, vocabulary=82, coherence=74, register=58),
        ]
        insight = assessment_insights(attempts)
        self.assertEqual("grammar", insight["weakest_dimension"])
        argumentation = next(item for item in insight["priority_topics"] if item["topic"] == "argumentation")
        self.assertEqual("grammar", argumentation["dimension"])
        self.assertLess(argumentation["score"], 70)
        gate = evidence_gate(attempts)
        self.assertFalse(gate["eligible"])
        self.assertEqual("repair_needed", gate["status"])
        self.assertIn("grammar", gate["gaps"])

    def test_independent_improvement_can_clear_progression_gate(self):
        repaired = [
            production("argumentation", task_completion=78, grammar=72, vocabulary=82, coherence=68, register=72),
            production("argumentation", task_completion=84, grammar=76, vocabulary=86, coherence=74, register=76),
            production("argumentation", task_completion=86, grammar=80, vocabulary=88, coherence=78, register=80),
        ]
        gate = evidence_gate(repaired)
        self.assertTrue(gate["eligible"])
        self.assertEqual("ready", gate["status"])
        self.assertEqual([], gate["gaps"])

    def test_diagnostic_routes_stay_stable_from_a1_through_b2(self):
        expected = {"A1": "A1", "A1+": "A1", "A2": "A2", "B1": "B1", "B1+": "B1", "B2": "B2"}
        self.assertEqual(expected, {level: curriculum_track_for_level(level) for level in expected})

    def test_realistic_mistake_history_changes_recommendation_and_recovers(self):
        first = lesson(1, "word_order", 1, "A2")
        articles = lesson(2, "articles", 2, "A2")
        route = [first, articles]
        mastery = {"word_order": 82, "articles": 72}
        history = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "word_order", "correct": True},
            {"skill_id": "articles", "correct": False},
        ]
        focus = repeated_error_focus(history, {item.topic for item in route})
        self.assertEqual("articles", focus)
        self.assertIs(
            select_recommended_lesson(route, set(), mastery, {}, focus_skill=focus),
            articles,
        )
        recovered = history + [
            {"skill_id": "articles", "correct": True},
            {"skill_id": "articles", "correct": True},
        ]
        self.assertIsNone(repeated_error_focus(recovered, {item.topic for item in route}))
        self.assertIs(
            select_recommended_lesson(route, set(), mastery, {},
                                      focus_skill=repeated_error_focus(recovered, {item.topic for item in route})),
            first,
        )

    def test_repeated_errors_do_not_unlock_prerequisite_or_cross_track(self):
        first = lesson(1, "word_order", 1, "A2")
        articles = lesson(2, "articles", 2, "A2", prerequisites=["word_order"])
        route = [first, articles]
        history = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": False},
            {"skill_id": "b2_argumentation", "correct": False},
            {"skill_id": "b2_argumentation", "correct": False},
        ]
        focus = repeated_error_focus(history, {item.topic for item in route})
        self.assertEqual("articles", focus)
        self.assertIs(select_recommended_lesson(route, set(), {}, {}, focus_skill=focus), first)
        self.assertEqual([1, 2], [item.id for item in route])

    def test_weak_ready_skill_can_be_prioritized_without_reordering_route(self):
        personal = lesson(10, "personal_details", 3, "A2", ["personal_details"])
        cases = lesson(11, "accusative_case", 4, "A2", ["accusative_case"])
        route = [personal, cases]
        picked = select_recommended_lesson(route, set(), {"personal_details": 66, "accusative_case": 61}, {"accusative_case": 5}, {"personal_details": 66, "accusative_case": 48})
        self.assertIs(picked, cases)
        self.assertEqual([10, 11], [item.id for item in route])


if __name__ == "__main__":
    unittest.main()
