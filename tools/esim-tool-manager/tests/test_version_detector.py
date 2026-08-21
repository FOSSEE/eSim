import subprocess
import unittest
from unittest.mock import patch, MagicMock

from esim_tool_manager.core import ToolSpec, VersionDetector


class TestVersionDetector(unittest.TestCase):

    def _spec(self, regex):
        return ToolSpec(
            name="ngspice",
            version_check_cmd=["ngspice", "-v"],
            version_regex=regex,
            latest_known_version="42",
        )

    @patch("esim_tool_manager.core.shutil.which", return_value=None)
    def test_returns_none_when_binary_missing(self, _mock_which):
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertIsNone(VersionDetector.get_installed_version(spec))

    @patch("esim_tool_manager.core.subprocess.run")
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/ngspice")
    def test_parses_hyphenated_version(self, _mock_which, mock_run):
        mock_run.return_value = MagicMock(stdout="ngspice-42\n", stderr="")
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertEqual(VersionDetector.get_installed_version(spec), "42")

    @patch("esim_tool_manager.core.subprocess.run")
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/ngspice")
    def test_parses_dotted_version(self, _mock_which, mock_run):
        mock_run.return_value = MagicMock(stdout="ngspice-42.1\n", stderr="")
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertEqual(VersionDetector.get_installed_version(spec), "42.1")

    @patch("esim_tool_manager.core.subprocess.run")
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/ngspice")
    def test_parses_verbose_version_string(self, _mock_which, mock_run):
        mock_run.return_value = MagicMock(stdout="ngspice version 42\n", stderr="")
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertEqual(VersionDetector.get_installed_version(spec), "42")

    @patch("esim_tool_manager.core.subprocess.run")
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/ngspice")
    def test_unknown_when_regex_does_not_match(self, _mock_which, mock_run):
        mock_run.return_value = MagicMock(stdout="totally unexpected output", stderr="")
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertEqual(VersionDetector.get_installed_version(spec), "unknown")

    @patch("esim_tool_manager.core.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="x", timeout=10))
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/ngspice")
    def test_handles_timeout_gracefully(self, _mock_which, _mock_run):
        spec = self._spec(r"ngspice[- ](?:version )?(\d+(?:\.\d+)*)")
        self.assertIsNone(VersionDetector.get_installed_version(spec))


if __name__ == "__main__":
    unittest.main()
