import unittest
from types import SimpleNamespace

from app.services.pro_funnel import pro_interest_funnel


class ProInterestFunnelTests(unittest.TestCase):
    def test_unique_users_and_repeat_clicks(self):
        events = [
            SimpleNamespace(user_id=1, event_name="pro_preview_viewed"),
            SimpleNamespace(user_id=1, event_name="pro_preview_viewed"),
            SimpleNamespace(user_id=2, event_name="pro_preview_viewed"),
            SimpleNamespace(user_id=1, event_name="pro_interest_clicked"),
            SimpleNamespace(user_id=1, event_name="pro_interest_clicked"),
            SimpleNamespace(user_id=3, event_name="pro_interest_clicked"),
        ]
        result = pro_interest_funnel(events)
        self.assertEqual(result["preview_users"], 2)
        self.assertEqual(result["interest_users"], 2)
        self.assertEqual(result["preview_to_interest_users"], 1)
        self.assertEqual(result["conversion_percent"], 50.0)
        self.assertEqual(result["preview_events"], 3)
        self.assertEqual(result["interest_events"], 3)

    def test_empty_window_is_safe(self):
        result = pro_interest_funnel([])
        self.assertEqual(result["conversion_percent"], 0)
        self.assertEqual(result["preview_users"], 0)


if __name__ == "__main__":
    unittest.main()
