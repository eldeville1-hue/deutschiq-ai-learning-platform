import unittest


class CloudRuntimeHelpersTest(unittest.TestCase):
    def test_public_origin_removes_path_and_query(self):
        from app.core.cloud_runtime import public_origin

        self.assertEqual(public_origin("https://example.com/app?v=2"), "https://example.com")

    def test_webhook_secret_comparison(self):
        from app.core.cloud_runtime import secret_matches

        self.assertTrue(secret_matches("same-secret", "same-secret"))
        self.assertFalse(secret_matches("wrong-secret", "same-secret"))
        self.assertFalse(secret_matches(None, "same-secret"))


if __name__ == "__main__":
    unittest.main()
