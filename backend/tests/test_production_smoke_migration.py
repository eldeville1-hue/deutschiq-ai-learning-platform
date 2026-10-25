"""Release smoke must reject unhealthy or mismatched database revisions."""
import unittest

from scripts.smoke_test import assert_database_release_ready


class ProductionSmokeMigrationTests(unittest.TestCase):
    EXPECTED = "20261023_0012"

    def test_current_migration_is_release_ready(self):
        assert_database_release_ready(
            {"status": "ok", "database": "ok", "migrations": self.EXPECTED},
            self.EXPECTED,
        )

    def test_old_migration_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Database is not release-ready"):
            assert_database_release_ready(
                {"status": "ok", "database": "ok", "migrations": "20261003_0011"},
                self.EXPECTED,
            )

    def test_database_unavailable_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Database is not release-ready"):
            assert_database_release_ready(
                {"status": "degraded", "database": "unavailable", "migrations": self.EXPECTED},
                self.EXPECTED,
            )

    def test_missing_migration_is_rejected(self):
        for revision in ("missing", "unknown", None):
            with self.subTest(revision=revision):
                with self.assertRaisesRegex(RuntimeError, "Database is not release-ready"):
                    assert_database_release_ready(
                        {"status": "degraded", "database": "ok", "migrations": revision},
                        self.EXPECTED,
                    )


if __name__ == "__main__":
    unittest.main()
