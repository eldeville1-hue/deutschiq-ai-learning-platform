import unittest
from types import SimpleNamespace
from app.services.learning_engine import mastery_update, mastery_update_from_evidence, next_stability, retention_score, review_interval, session_score, summarize_attempts
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

    def test_mastery_is_bounded_and_confidence_weighted(self):
        self.assertEqual(mastery_update(95, True, "sure"), 100)
        self.assertLess(mastery_update(50, True, "guess"), mastery_update(50, True, "sure"))
        self.assertEqual(mastery_update(3, False, "okay"), 0)

    def test_production_mastery_uses_rubric_strength(self):
        self.assertGreater(mastery_update_from_evidence(50, 92, "okay"), mastery_update_from_evidence(50, 72, "okay"))
        self.assertLess(mastery_update_from_evidence(50, 45, "okay"), 50)

    def test_review_intervals_expand(self):
        self.assertEqual(review_interval(False, 8), 1)
        self.assertEqual(review_interval(True, 1), 1)
        self.assertEqual(review_interval(True, 5), 30)

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

    def test_recommendation_adapts_without_reordering_route(self):
        first = SimpleNamespace(id=1, topic="word_order", content={"day": 1}, weak_point_tags=["word_order"])
        articles = SimpleNamespace(id=2, topic="articles", content={"day": 15}, weak_point_tags=["articles"])
        lessons = [first, articles]
        picked = select_recommended_lesson(lessons, set(), {"word_order": 60}, {"articles": 9})
        self.assertEqual([item.id for item in lessons], [1, 2])
        self.assertIs(picked, articles)


if __name__ == "__main__":
    unittest.main()
