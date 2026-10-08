import unittest
from tests.prepare_ai_workload_v88 import prepare, LEVELS, MIN_PER_LEVEL


class AiWorkloadTests(unittest.TestCase):
    def test_balanced_development_workload_is_not_release_attestation(self):
        manifest = prepare()
        self.assertEqual(manifest["sample_count"], 100)
        self.assertFalse(manifest["validation_errors"])
        self.assertFalse(manifest["representative_release_sample"])
        self.assertFalse(manifest["independently_reviewed"])
        for level in LEVELS:
            self.assertEqual(manifest["counts_by_level"][level], MIN_PER_LEVEL)
        self.assertTrue(all(row["exercise"]["question"] for row in manifest["cases"]))

    def test_missing_level_blocks_workload(self):
        rows = [{"cefr": "A1", "id": "one", "learner_answer": "Hallo",
                 "objective": "Say hello", "exercise": {"answer": "Hallo"}}]
        manifest = prepare(rows)
        self.assertTrue(manifest["validation_errors"])
        self.assertFalse(manifest["representative_release_sample"])


if __name__ == "__main__":
    unittest.main()
