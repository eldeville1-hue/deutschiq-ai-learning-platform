import unittest

from seed_30_day_plan import CURRICULUM, GOLD_RETRY_SENTENCES, build_content
from app.services.lesson_coaching import supported_retry_exercise


class AuthoredRoadmapRetryTests(unittest.TestCase):
    def test_all_thirty_lessons_have_distinct_skill_aligned_retries(self):
        self.assertEqual(set(range(1, 31)), set(GOLD_RETRY_SENTENCES))
        for day, topic, rule, _tag, example, question, answer in CURRICULUM:
            with self.subTest(day=day):
                content = build_content(day, topic, rule, example, question, answer)
                skill = CURRICULUM[day - 1][3]
                self.assertEqual(2, len(content["retry_examples"]))
                self.assertTrue(all(item["skill_id"] == skill for item in content["retry_examples"]))
                guided = content["exercises"][0]
                self.assertEqual(skill, guided["skill_id"])
                retry = supported_retry_exercise(guided, content, "de")
                self.assertIsNotNone(retry)
                self.assertIn(retry["answer"], [item["sentence"].rstrip(".?!") for item in content["retry_examples"]])
                self.assertNotEqual(retry["answer"].casefold(), str(answer).rstrip(".?!").casefold())
                self.assertNotEqual(retry["tokens"], retry["answer"].split())


if __name__ == "__main__":
    unittest.main()
