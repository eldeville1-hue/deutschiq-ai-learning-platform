import unittest

from app.services.lesson_coaching import feedback_focus, learning_profile, repair_plan, success_feedback, supported_retry_exercise


class LessonCoachingTests(unittest.TestCase):
    def test_retry_uses_first_example_when_second_is_original_answer(self):
        retry = supported_retry_exercise({"answer": "Ich wohne in Berlin."},
            {"examples": ["Ich wohne in Hamburg.", "Ich wohne in Berlin."], "rule": "Das Verb steht auf Position zwei."}, "en")
        self.assertEqual("Ich wohne in Hamburg", retry["answer"])
        self.assertEqual("Das Verb steht auf Position zwei.", retry["explanation"])

    def test_retry_normalizes_punctuation_before_claiming_a_fresh_example(self):
        retry = supported_retry_exercise({"answer": "Ich lerne Deutsch."},
            {"examples": ["Ich lerne Deutsch!", "Ich lerne Englisch."]}, "de")
        self.assertEqual("Ich lerne Englisch", retry["answer"])

    def test_retry_does_not_claim_new_context_when_only_original_model_exists(self):
        for lang in ('ru', 'de', 'en'):
            retry = supported_retry_exercise({"answer": "Ich lerne Deutsch."}, {"examples": ["Ich lerne Deutsch."]}, lang)
            self.assertIsNone(retry)

    def test_retry_without_any_authored_examples_is_not_duplicated(self):
        retry = supported_retry_exercise({"answer": "Du hast Zeit."}, {}, "de")
        self.assertIsNone(retry)

    def test_supported_retry_uses_a_fresh_sentence_and_localized_phone_prompt(self):
        exercise = {"id": "obwohl-guided", "answer": "Obwohl es regnet, gehen wir spazieren.", "accepted_answers": ["Obwohl es regnet, gehen wir spazieren."], "misconception": "verb_not_final"}
        content = {"examples": ["Obwohl es regnet, gehen wir spazieren.", "Obwohl ich müde bin, gehe ich zum Kurs."]}
        retry = supported_retry_exercise(exercise, content, "de")
        self.assertEqual("reorder", retry["type"])
        self.assertEqual("Obwohl ich müde bin, gehe ich zum Kurs", retry["answer"])
        self.assertNotEqual(retry["tokens"], retry["answer"].split())
        self.assertIn("neuen Beispiel", retry["question"])
    def test_retry_prefers_authored_example_with_matching_pattern(self):
        retry = supported_retry_exercise(
            {"answer": "Ich muss heute Deutsch lernen."},
            {"examples": [
                "Obwohl es regnet, gehe ich spazieren.",
                "Ich muss morgen Deutsch lernen.",
                "Ich muss heute Deutsch lernen.",
            ]}, "en")
        self.assertEqual("Ich muss morgen Deutsch lernen", retry["answer"])
        self.assertNotIn("Ich muss heute Deutsch lernen", retry["accepted_answers"])

    def test_explicit_skill_tag_outweighs_surface_similarity(self):
        retry = supported_retry_exercise(
            {"answer": "Ich muss heute Deutsch lernen.", "skill_id": "modal-infinitive"},
            {"examples": ["Ich muss morgen Deutsch lernen."], "retry_examples": [
                {"skill_id": "modal-infinitive", "sentence": "Du kannst heute schwimmen."},
                {"skill_id": "past-tense", "sentence": "Ich habe gestern Deutsch gelernt."},
            ]}, "en")
        self.assertEqual("Du kannst heute schwimmen", retry["answer"])

    def test_tagged_retry_bank_does_not_use_unrelated_skill(self):
        retry = supported_retry_exercise(
            {"answer": "Ich muss lernen.", "skill_id": "modal-infinitive"},
            {"examples": ["Ich habe gestern gelernt."], "retry_examples": [
                {"skill_id": "past-tense", "sentence": "Ich bin nach Hause gegangen."},
            ]}, "en")
        self.assertIsNone(retry)

    def test_exhausted_tagged_retry_does_not_repeat_or_switch_skill(self):
        retry = supported_retry_exercise(
            {"answer": "Du kannst heute kommen.", "skill_id": "modal-infinitive"},
            {"examples": ["Ich habe gestern gelernt."], "retry_examples": [
                {"skill_id": "modal-infinitive", "sentence": "Du kannst heute kommen."},
                {"skill_id": "past-tense", "sentence": "Ich bin nach Hause gegangen."},
            ]}, "de")
        self.assertIsNone(retry)

    def test_retry_keeps_answer_key_and_does_not_mutate_source(self):
        exercise = {"id": "guided", "answer": "Ich muss heute lernen.", "skill_id": "modal"}
        lesson = {"examples": ["Ich muss heute lernen."], "retry_examples": [
            {"skill_id": "modal", "sentence": "Du kannst morgen kommen."}
        ]}
        retry = supported_retry_exercise(exercise, lesson, "de")
        self.assertEqual("Du kannst morgen kommen", retry["answer"])
        self.assertEqual(["Du kannst morgen kommen", "Du kannst morgen kommen."], retry["accepted_answers"])
        self.assertNotIn("tokens", exercise)
        self.assertEqual("Du kannst morgen kommen.", lesson["retry_examples"][0]["sentence"])

    def test_retry_does_not_offer_one_word_reordering(self):
        retry = supported_retry_exercise(
            {"answer": "Hallo."}, {"examples": ["Danke."]}, "de")
        self.assertIsNone(retry)

    def test_retry_does_not_offer_identical_repeated_word_order(self):
        retry = supported_retry_exercise(
            {"answer": "Hallo."}, {"examples": ["Ja ja."]}, "de")
        self.assertIsNone(retry)

    def test_retry_with_repeated_tokens_is_shuffled(self):
        retry = supported_retry_exercise(
            {"answer": "Hallo."}, {"examples": ["Ja ja nein nein."]}, "de")
        self.assertIsNotNone(retry)
        self.assertNotEqual(retry["tokens"], retry["answer"].split())

    def test_struggling_learner_gets_supported_mode(self):
        profile = learning_profile(60, [True, False, False], 0)
        self.assertEqual("supported", profile["mode"])
        self.assertTrue(profile["show_guided_hint"])

    def test_mastered_learner_gets_challenge_mode(self):
        profile = learning_profile(82, [True, True, True], 3)
        self.assertEqual("challenge", profile["mode"])
        self.assertFalse(profile["show_guided_hint"])

    def test_repair_plan_uses_actual_missing_words_and_language(self):
        steps = repair_plan("missing_words", ["habe", "gearbeitet"], [], "de")
        self.assertEqual(3, len(steps))
        self.assertIn("habe", steps[1])
        self.assertIn("Wortstellung", steps[2])

    def test_feedback_focus_names_the_smallest_action_without_revealing_model(self):
        self.assertEqual("Ergänze: habe, gearbeitet.", feedback_focus("missing_words", ["habe", "gearbeitet"], [], "de"))
        self.assertEqual("Remove or replace: is.", feedback_focus("answer_mismatch", [], ["is"], "en"))
        self.assertIn("порядок", feedback_focus("answer_mismatch", [], [], "ru"))

    def test_success_feedback_has_localized_fallback(self):
        self.assertEqual("Die Verbform ist richtig.", success_feedback(" Die Verbform ist richtig. ", "de"))
        self.assertIn("situation", success_feedback("", "en").lower())


if __name__ == "__main__":
    unittest.main()
