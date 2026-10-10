import unittest
from types import SimpleNamespace
from app.services.learning_engine import adaptive_mastery_update, adaptive_priority_score, mastery_update, mastery_update_from_evidence, next_stability, retention_score, retrieval_review_interval, review_interval, session_score, summarize_attempts, summarize_mission
from app.services.skill_graph import blocked_by, prerequisites_met
from app.services.learning_route import lesson_blockers, select_recommended_lesson


class LearningEngineTests(unittest.TestCase):
    def test_score_uses_only_given_session(self):
        self.assertEqual(session_score([True, False, True]), 67)
        self.assertEqual(session_score([]), 0)

    def test_corrected_retry_counts_as_learning_not_a_permanent_failure(self):
        attempts = [
            SimpleNamespace(exercise_index=0, correct=False),
            SimpleNamespace(exercise_index=0, correct=True),
            SimpleNamespace(exercise_index=1, correct=True),
        ]
        summary = summarize_attempts(attempts)
        self.assertEqual(100, summary["score"])
        self.assertEqual(1, summary["first_try_correct"])
        self.assertEqual(1, summary["corrected_retries"])
        self.assertEqual(0, summary["needs_review"])

    def test_mission_requires_independent_production_evidence(self):
        attempts = [
            SimpleNamespace(exercise_index=3, correct=False, production_score=48, answer="Ich Hamburg."),
            SimpleNamespace(exercise_index=3, correct=True, production_score=None, answer="Ich wohne in Hamburg."),
        ]
        summary = summarize_mission(attempts, 3)
        self.assertTrue(summary["mission_attempted"])
        self.assertFalse(summary["mission_passed"])
        self.assertEqual(48, summary["mission_score"])
        self.assertEqual("Ich Hamburg.", summary["mission_answer"])

    def test_mission_passes_with_strong_independent_answer(self):
        attempts = [SimpleNamespace(
            exercise_index=3, correct=True, production_score=86,
            answer="Ich komme aus Kyjiw und wohne in Hamburg.",
        )]
        summary = summarize_mission(attempts, 3)
        self.assertTrue(summary["mission_passed"])
        self.assertEqual(86, summary["mission_score"])

    def test_mastery_is_bounded_and_confidence_weighted(self):
        self.assertEqual(mastery_update(95, True, "sure"), 100)
        self.assertLess(mastery_update(50, True, "guess"), mastery_update(50, True, "sure"))
        self.assertEqual(mastery_update(3, False, "okay"), 0)

    def test_production_mastery_uses_rubric_strength(self):
        self.assertGreater(mastery_update_from_evidence(50, 92, "okay"), mastery_update_from_evidence(50, 72, "okay"))
        self.assertLess(mastery_update_from_evidence(50, 45, "okay"), 50)

    def test_supported_retry_grows_mastery_less_than_independent_recall(self):
        independent = adaptive_mastery_update(40, True, "sure")
        supported_retry = adaptive_mastery_update(40, True, "sure", retry=True)
        self.assertGreater(independent, supported_retry)
        self.assertGreater(supported_retry, 40)

    def test_delayed_retrieval_is_stronger_positive_evidence(self):
        lesson_gain = adaptive_mastery_update(40, True, "sure")
        retrieval_gain = adaptive_mastery_update(40, True, "sure", retrieval=True)
        self.assertGreater(retrieval_gain, lesson_gain)

    def test_errors_are_not_softened_by_evidence_mode(self):
        regular = adaptive_mastery_update(50, False, "sure")
        retry_error = adaptive_mastery_update(50, False, "sure", retry=True)
        review_error = adaptive_mastery_update(50, False, "sure", retrieval=True)
        self.assertEqual(regular, retry_error)
        self.assertEqual(regular, review_error)

    def test_adaptive_priority_uses_retention_decay(self):
        self.assertEqual(70, adaptive_priority_score(70, 7, 0))
        self.assertLess(adaptive_priority_score(70, 7, 5), 70)

    def test_review_intervals_expand(self):
        self.assertEqual(review_interval(False, 8), 1)
        self.assertEqual(review_interval(True, 1), 1)
        self.assertEqual(review_interval(True, 5), 30)

    def test_retrieval_schedule_uses_stability_and_a_lapse_returns_tomorrow(self):
        self.assertEqual(1, retrieval_review_interval(False, 20))
        self.assertEqual(3, retrieval_review_interval(True, 1.8))
        self.assertEqual(7, retrieval_review_interval(True, 7.2))
        self.assertEqual(30, retrieval_review_interval(True, 90))

    def test_confident_error_is_penalized_more_than_guess(self):
        self.assertLess(mastery_update(50, False, "sure"), mastery_update(50, False, "guess"))

    def test_slow_correct_recall_grows_less(self):
        self.assertLess(mastery_update(40, True, "okay", 60_000), mastery_update(40, True, "okay", 5_000))

    def test_retention_decays_when_review_is_overdue(self):
        self.assertEqual(retention_score(70, 7, 0), 70)
        self.assertLess(retention_score(70, 7, 5), 70)

    def test_stability_recovers_and_collapses(self):
        self.assertGreater(next_stability(3, True, "sure"), 3)
        self.assertLess(next_stability(10, False, "sure"), 10)

    def test_skill_graph_blocks_advanced_topic(self):
        self.assertFalse(prerequisites_met("dative_case", {"word_order": 20}))
        self.assertEqual(blocked_by("dative_case", {"word_order": 20}), ["word_order"])

    def test_route_keeps_repeated_skill_steps_sequential(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        second = SimpleNamespace(id=2, topic="word_order", content={"day": 2}, weak_point_tags=["word_order"])
        lessons = [first, second]
        self.assertEqual(lesson_blockers(second, lessons, set(), {}), ["previous_step"])
        self.assertIs(select_recommended_lesson(lessons, set(), {}, {"word_order": 9}), first)
        self.assertIs(select_recommended_lesson(lessons, {1}, {}, {"word_order": 9}), second)

    def test_completed_lesson_never_becomes_locked_again(self):
        lesson = SimpleNamespace(id=8, topic="dative_case", content={"day": 8}, weak_point_tags=["dative_case"])
        self.assertEqual(lesson_blockers(lesson, [lesson], {8}, {"word_order": 0}), [])

    def test_declared_curriculum_prerequisite_is_actually_enforced(self):
        first = SimpleNamespace(id=1, topic="greetings", content={"day": 1, "track": "A1", "prerequisites": []}, weak_point_tags=["greetings"])
        second = SimpleNamespace(id=2, topic="personal_details", content={"day": 2, "track": "A1", "prerequisites": ["greetings"]}, weak_point_tags=["personal_details"])
        self.assertEqual(["previous_step"], lesson_blockers(second, [first, second], set(), {}))
        self.assertEqual([], lesson_blockers(second, [first, second], {1}, {}))
        self.assertEqual([], lesson_blockers(second, [first, second], set(), {"greetings": 72}))

    def test_recommendation_can_prioritize_forgotten_skill_without_relocking_route(self):
        stable = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=[])
        fading = SimpleNamespace(id=2, topic="articles", content={"day": 2}, weak_point_tags=[])
        lessons = [stable, fading]
        mastery = {"word_order": 75, "articles": 80}
        retained_strength = {"word_order": 72, "articles": 45}
        picked = select_recommended_lesson(lessons, set(), mastery, {}, retained_strength)
        self.assertIs(picked, fading)

    def test_repeated_error_focus_prioritizes_available_skill(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        second = SimpleNamespace(id=2, topic="articles", content={"day": 2}, weak_point_tags=["articles"])
        lessons = [first, second]
        picked = select_recommended_lesson(lessons, set(), {"word_order": 80}, {}, focus_skill="articles")
        self.assertIs(picked, second)
        self.assertEqual([1, 2], [lesson.id for lesson in lessons])

    def test_repeated_error_focus_never_bypasses_blockers(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        second = SimpleNamespace(id=2, topic="word_order", content={"day": 2}, weak_point_tags=["word_order"])
        lessons = [first, second]
        self.assertIs(select_recommended_lesson(lessons, set(), {}, {},
                                                focus_skill="word_order"), first)

    def test_unknown_focus_keeps_existing_priority(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        second = SimpleNamespace(id=2, topic="articles", content={"day": 2}, weak_point_tags=["articles"])
        lessons = [first, second]
        self.assertIs(select_recommended_lesson(lessons, set(), {}, {},
                                                focus_skill="not_in_route"), first)

    def test_recommendation_adapts_without_reordering_route(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        articles = SimpleNamespace(id=2, topic="articles", content={"day": 15}, weak_point_tags=["articles"])
        lessons = [first, articles]
        picked = select_recommended_lesson(lessons, set(), {"word_order": 60}, {"articles": 9})
        self.assertEqual([item.id for item in lessons], [1, 2])
        self.assertIs(picked, articles)


if __name__ == "__main__":
    unittest.main()
