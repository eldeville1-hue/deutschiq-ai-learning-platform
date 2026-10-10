import re
import unittest

from seed_30_day_plan import CURRICULUM, GOLD_RETRY_TARGETS, build_content
from app.services.lesson_coaching import supported_retry_exercise


class AuthoredRetryTargetTests(unittest.TestCase):
    def test_curated_targets_exist_in_their_sentences(self):
        for day, targets in GOLD_RETRY_TARGETS.items():
            content = build_content(*[CURRICULUM[day - 1][0], CURRICULUM[day - 1][1], CURRICULUM[day - 1][2], CURRICULUM[day - 1][4], CURRICULUM[day - 1][5], CURRICULUM[day - 1][6]])
            self.assertEqual(2, len(targets))
            for item, target in zip(content["retry_examples"], targets):
                with self.subTest(day=day, target=target):
                    self.assertIn(target, re.findall(r"\b[\wÄÖÜäöüß]+\b", item["sentence"]))
                    self.assertEqual(target, item["target"])

    def test_retry_blanks_authored_target_not_unrelated_article(self):
        for day in (8, 9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30):
            row = CURRICULUM[day - 1]
            content = build_content(row[0], row[1], row[2], row[4], row[5], row[6])
            retry = supported_retry_exercise(content["exercises"][0], content, "en")
            with self.subTest(day=day):
                self.assertIsNotNone(retry)
                self.assertEqual("fill", retry["type"])
                self.assertIn(retry["answer"], GOLD_RETRY_TARGETS[day])


if __name__ == "__main__":
    unittest.main()
