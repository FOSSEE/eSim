import unittest
from unittest.mock import patch

from tools.esim_tool_manager.detector import ToolDetector


class TestToolDetector(unittest.TestCase):

    def test_detect_installed_tool(self):
        detector = ToolDetector()

        with patch(
            "shutil.which",
            return_value="/usr/bin/ngspice",
        ):
            with patch.object(
                detector,
                "_get_version",
                return_value="ngspice version 45.2",
            ):
                result = detector.detect_tool(
                    "ngspice",
                    "ngspice",
                )

        self.assertTrue(result.installed)
        self.assertEqual(result.name, "ngspice")
        self.assertEqual(
            result.version,
            "ngspice version 45.2",
        )

    def test_detect_missing_tool(self):
        detector = ToolDetector()

        with patch(
            "shutil.which",
            return_value=None,
        ):
            result = detector.detect_tool(
                "ngspice",
                "ngspice",
            )

        self.assertFalse(result.installed)
        self.assertIsNone(result.version)

    def test_supported_tools(self):
        detector = ToolDetector()

        self.assertIn("ngspice", detector.TOOLS)
        self.assertIn("verilator", detector.TOOLS)
        self.assertIn("ghdl", detector.TOOLS)
        self.assertIn("kicad", detector.TOOLS)


if __name__ == "__main__":
    unittest.main()
