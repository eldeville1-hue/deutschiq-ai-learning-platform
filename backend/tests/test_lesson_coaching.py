import unittest

from app.services.lesson_coaching import feedback_focus, learning_profile, repair_plan, success_feedback, supported_retry_exercise, repeated_error_focus


class FeedbackLanguageQualityTests(unittest.TestCase):
    """Check meaningful guidance in each supported interface language."""

    def test_verb_final_hint_identifies_subordinate_clause_in_every_language(self):
        expected = {
            "ru": ("глагол", "придаточного"),
            "de": ("Verb", "Nebensatzes"),
            "en": ("verb", "subordinate clause"),
        }
        for lang, terms in expected.items():
            with self.subTest(language=lang):
                hint = feedback_focus("verb_not_final", ["geht"], ["gehen"], lang)
                self.assertTrue(all(term in hint for term in terms))
                self.assertNotIn("Add:", hint)

    def test_article_hint_mentions_gender_number_and_case(self):
        expected = {
            "ru": ("род", "число", "падеж"),
            "de": ("Genus", "Numerus", "Kasus"),
            "en": ("gender", "number", "case"),
        }
        for lang, terms in expected.items():
            with self.subTest(language=lang):
                hint = feedback_focus("article", ["der"], ["die"], lang).lower()
                self.assertTrue(all(term.lower() in hint for term in terms))

    def test_case_hint_does_not_expose_model_answer(self):
        for lang in ("ru", "de", "en"):
            with self.subTest(language=lang):
                hint = feedback_focus("case", ["dem"], ["den"], lang)
                import re
                tokens = re.findall(r"\b\w+\b", hint.casefold())
                self.assertNotIn("dem", tokens)
                # "den" is also a normal article in German instructions.
                # Its occurrence alone does not reveal the correct case form.
                if lang != "de":
                    self.assertNotIn("den", tokens)


class RepeatedErrorFocusTests(unittest.TestCase):
    def test_recent_unresolved_mistake_wins_over_older_error(self):
        attempts = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": False},
            {"skill_id": "word_order", "correct": False},
            {"skill_id": "word_order", "correct": False},
        ]
        self.assertEqual("word_order", repeated_error_focus(attempts))

    def test_recent_correction_reduces_urgency(self):
        attempts = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": True},
            {"skill_id": "word_order", "correct": False},
            {"skill_id": "word_order", "correct": False},
        ]
        self.assertEqual("word_order", repeated_error_focus(attempts))

    def test_never_focuses_on_single_error_or_unavailable_skill(self):
        attempts = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "word_order", "correct": False},
            {"skill_id": "word_order", "correct": False},
        ]
        self.assertIsNone(repeated_error_focus(attempts, {"articles"}))


class GrammarRuleFirstFeedbackTests(unittest.TestCase):
    def test_case_feedback_prioritizes_rule(self):
        result = feedback_focus("case", ["dem"], ["den"], "en")
        self.assertIn("required case", result)
        self.assertNotIn("Add:", result)

    def test_article_feedback_prioritizes_gender_number_case(self):
        result = feedback_focus("article", ["die"], ["der"], "de")
        self.assertIn("Genus, Numerus und Kasus", result)

    def test_conjugation_feedback_prioritizes_subject_agreement(self):
        result = feedback_focus("conjugation", ["geht"], ["gehen"], "en")
        self.assertIn("subject", result)

    def test_unknown_error_preserves_word_level_guidance(self):
        self.assertIn("Add: bitte", feedback_focus("unknown_error", ["bitte"], [], "en"))


class WordOrderFeedbackTests(unittest.TestCase):
    def test_word_order_error_prioritizes_structure_over_token_diff(self):
        self.assertIn("order", feedback_focus("word_order", ["hat"], ["haben"], "en"))

    def test_word_order_hint_does_not_claim_all_words_are_present(self):
        for lang in ("ru", "de", "en"):
            hint = feedback_focus("word_order", ["hat"], ["haben"], lang)
            self.assertNotIn("All required words are present", hint)
            self.assertNotIn("Alle nötigen Wörter sind da", hint)
            self.assertNotIn("Все нужные слова есть", hint)

    def test_verb_final_error_prioritizes_sentence_structure(self):
        self.assertIn("Ende des Nebensatzes", feedback_focus("verb_not_final", ["geht"], [], "de"))

    def test_missing_word_still_gets_specific_guidance(self):
        self.assertIn("Add: bitte", feedback_focus("missing_word", ["bitte"], [], "en"))


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

    def test_case_retry_asks_for_missing_article_not_word_order(self):
        retry = supported_retry_exercise(
            {"answer": "Ich helfe dem Mann.", "skill_id": "dative_case"},
            {"retry_examples": [{"skill_id": "dative_case",
                                 "sentence": "Sie hilft der Frau."}]}, "de")
        self.assertEqual("fill", retry["type"])
        self.assertEqual("der", retry["answer"])
        self.assertIn("Sie hilft ___ Frau", retry["question"])
        self.assertNotIn("tokens", retry)

    def test_perfect_retry_asks_for_auxiliary(self):
        retry = supported_retry_exercise(
            {"answer": "Ich habe gegessen.", "skill_id": "perfekt_auxiliary"},
            {"retry_examples": [{"skill_id": "perfekt_auxiliary",
                                 "sentence": "Wir sind früh angekommen."}]}, "en")
        self.assertEqual("fill", retry["type"])
        self.assertEqual("sind", retry["answer"])
        self.assertIn("Wir ___ früh angekommen", retry["question"])

    def test_form_retry_without_safe_target_does_not_become_reorder(self):
        retry = supported_retry_exercise(
            {"answer": "Ich helfe dem Mann.", "skill_id": "dative_case"},
            {"retry_examples": [{"skill_id": "dative_case",
                                 "sentence": "Wir helfen unseren Freunden."}]}, "de")
        self.assertIsNone(retry)

    def test_form_retry_with_invalid_authored_target_does_not_guess(self):
        retry = supported_retry_exercise(
            {"answer": "Ich habe gegessen.", "skill_id": "perfekt_auxiliary"},
            {"retry_examples": [{"skill_id": "perfekt_auxiliary",
                                 "sentence": "Wir sind angekommen.", "target": "habe"}]}, "en")
        self.assertIsNone(retry)

    def test_repeated_mistakes_select_a_skill_for_followup(self):
        attempts = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "word_order", "correct": False},
            {"skill_id": "articles", "correct": False},
        ]
        profile = learning_profile(55, [False, True, False], recent_skill_attempts=attempts,
                                   available_skills={"articles", "word_order"})
        self.assertEqual("articles", profile["focus_skill"])

    def test_corrected_skill_does_not_remain_a_priority(self):
        attempts = [
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": False},
            {"skill_id": "articles", "correct": True},
            {"skill_id": "articles", "correct": True},
        ]
        self.assertIsNone(learning_profile(60, [], recent_skill_attempts=attempts)["focus_skill"])

    def test_unavailable_skills_are_not_selected(self):
        attempts = [{"skill_id": "articles", "correct": False}] * 3
        profile = learning_profile(50, [], recent_skill_attempts=attempts,
                                   available_skills={"word_order"})
        self.assertIsNone(profile["focus_skill"])

    def test_legacy_profile_without_history_remains_compatible(self):
        self.assertIsNone(learning_profile(60, [True])["focus_skill"])

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
