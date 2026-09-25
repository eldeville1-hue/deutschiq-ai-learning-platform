import unittest
from pathlib import Path


class FrontendInternationalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frontend = Path(__file__).resolve().parents[2] / "frontend" / "mini-app" / "src"

    def read(self, relative: str) -> str:
        return (self.frontend / relative).read_text(encoding="utf-8")

    def test_authentication_recovery_uses_selected_language(self):
        source = self.read("App.tsx")
        self.assertIn("tr(preferredLanguage", source)
        self.assertNotIn("Открой приложение через @DeutschIQ_bot · Öffne", source)

    def test_celebration_has_no_russian_only_user_copy(self):
        source = self.read("components/Celebration.tsx")
        self.assertIn("useLanguage", source)
        self.assertNotIn("Урок завершён!</h2>", source)
        self.assertNotIn("Продолжайте в том же духе", source)

    def test_tutor_history_is_requested_for_active_language(self):
        page = self.read("pages/Tutor.tsx")
        api = self.read("services/api.ts")
        self.assertIn("api.getTutorState(userId, lang)", page)
        self.assertIn("/api/tutor/state/${userId}?lang=${lang}", api)

    def test_diagnostic_and_mistakes_have_localized_retry_states(self):
        diagnostic = self.read("pages/Diagnostic.tsx")
        mistakes = self.read("pages/Mistakes.tsx")
        self.assertIn("questionError", diagnostic)
        self.assertIn("setQuestionRetry", diagnostic)
        self.assertIn("loadError", mistakes)
        self.assertIn("Erneut versuchen", mistakes)

    def test_document_language_and_metadata_follow_active_language(self):
        context = self.read("context/LanguageContext.tsx")
        index = (self.frontend.parent / "index.html").read_text(encoding="utf-8")
        self.assertIn("document.documentElement.lang = lang", context)
        self.assertIn("META_COPY", context)
        self.assertIn('<html lang="en">', index)

    def test_daily_session_connects_review_to_the_next_lesson(self):
        dashboard = self.read("pages/Dashboard.tsx")
        review = self.read("pages/Review.tsx")
        lesson = self.read("pages/Lesson.tsx")
        self.assertIn("/review?nextLesson=", dashboard)
        self.assertIn("useSearchParams", review)
        self.assertIn("exercise_retried", lesson)
        self.assertIn("corrected_retries", lesson)

    def test_mobile_reliability_has_offline_and_safe_cache_recovery(self):
        app = self.read("App.tsx")
        api = self.read("services/api.ts")
        self.assertIn("ConnectionStatus", app)
        self.assertIn("window.addEventListener('offline'", app)
        self.assertIn("const readCache", api)
        self.assertIn("const writeCache", api)

    def test_lesson_supports_context_listening_dialogue_and_error_repair(self):
        lesson = self.read("pages/Lesson.tsx")
        exercise_types = self.read("learning/exercises.ts")
        interaction = self.read("components/learning/ExerciseInteraction.tsx")
        self.assertIn("listening_choice", exercise_types)
        self.assertIn("dialogue", exercise_types)
        self.assertIn("error_repair", exercise_types)
        self.assertIn("ExerciseInteraction", lesson)
        self.assertIn("exerciseKind", interaction)
        self.assertIn("slice(0, 5)", lesson)

    def test_lesson_offers_low_pressure_mobile_alternatives(self):
        lesson = self.read("pages/Lesson.tsx")
        interaction = self.read("components/learning/ExerciseInteraction.tsx")
        self.assertIn("Make easier", lesson)
        self.assertIn("Skip for now", lesson)
        self.assertIn("I can't listen", lesson)
        self.assertIn("exercise_skipped", lesson)
        self.assertIn("Build the corrected sentence", interaction)
        self.assertIn("USE AS A STARTER", interaction)


if __name__ == "__main__":
    unittest.main()
