import unittest
from unittest.mock import patch

from tools.esim_tool_manager.update_checker import (
    UpdateChecker,
)


class TestUpdateChecker(unittest.TestCase):

    def test_compare_versions_update_available(self):
        checker = UpdateChecker()

        with patch(
            "subprocess.run"
        ) as mock_run:

            mock_run.return_value.returncode = 0

            result = checker.compare_versions(
                "1.0-1",
                "2.0-1",
            )

        self.assertTrue(result)

    def test_compare_versions_up_to_date(self):
        checker = UpdateChecker()

        with patch(
            "subprocess.run"
        ) as mock_run:

            mock_run.return_value.returncode = 1

            result = checker.compare_versions(
                "2.0-1",
                "2.0-1",
            )

        self.assertFalse(result)

    def test_compare_versions_missing_version(self):
        checker = UpdateChecker()

        self.assertFalse(
            checker.compare_versions(
                None,
                "2.0-1",
            )
        )

        self.assertFalse(
            checker.compare_versions(
                "1.0-1",
                None,
            )
        )


if __name__ == "__main__":
    unittest.main()
