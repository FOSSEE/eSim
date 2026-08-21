import unittest
from unittest.mock import patch

from esim_tool_manager.core import PlatformInfo


class TestPlatformInfo(unittest.TestCase):

    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/apt")
    @patch("esim_tool_manager.core.platform.system", return_value="Linux")
    def test_detects_apt_on_linux(self, _sys, _which):
        info = PlatformInfo()
        self.assertTrue(info.is_linux)
        self.assertEqual(info.package_manager, "apt")

    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/local/bin/brew")
    @patch("esim_tool_manager.core.platform.system", return_value="Darwin")
    def test_detects_brew_on_mac(self, _sys, _which):
        info = PlatformInfo()
        self.assertTrue(info.is_mac)
        self.assertEqual(info.package_manager, "brew")

    @patch("esim_tool_manager.core.shutil.which", return_value=r"C:\ProgramData\chocolatey\choco.exe")
    @patch("esim_tool_manager.core.platform.system", return_value="Windows")
    def test_detects_choco_on_windows(self, _sys, _which):
        info = PlatformInfo()
        self.assertTrue(info.is_windows)
        self.assertEqual(info.package_manager, "choco")

    @patch("esim_tool_manager.core.shutil.which", return_value=None)
    @patch("esim_tool_manager.core.platform.system", return_value="Linux")
    def test_no_package_manager_detected(self, _sys, _which):
        info = PlatformInfo()
        self.assertIsNone(info.package_manager)


if __name__ == "__main__":
    unittest.main()
