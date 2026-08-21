import unittest
from unittest.mock import patch

from esim_tool_manager.core import ToolManager, DEFAULT_REGISTRY


class TestRegistry(unittest.TestCase):

    def test_default_registry_has_expected_tools(self):
        for name in ("ngspice", "kicad", "ghdl"):
            self.assertIn(name, DEFAULT_REGISTRY)

    def test_each_spec_has_a_version_regex_and_check_cmd(self):
        for name, spec in DEFAULT_REGISTRY.items():
            self.assertTrue(spec["version_check_cmd"], f"{name} missing version_check_cmd")
            self.assertTrue(spec["version_regex"], f"{name} missing version_regex")

    @patch("esim_tool_manager.core.shutil.which", return_value=None)
    def test_unknown_tool_raises_value_error(self, _which):
        manager = ToolManager()
        with self.assertRaises(ValueError):
            manager._get_spec("definitely_not_a_real_tool")

    @patch("esim_tool_manager.core.shutil.which", return_value=None)
    def test_unknown_tool_error_lists_available_tools(self, _which):
        manager = ToolManager()
        try:
            manager._get_spec("nope")
        except ValueError as e:
            for name in DEFAULT_REGISTRY:
                self.assertIn(name, str(e))
        else:
            self.fail("Expected ValueError for unknown tool")


if __name__ == "__main__":
    unittest.main()
