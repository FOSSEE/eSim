import unittest
from unittest.mock import patch, MagicMock

from esim_tool_manager.core import ToolManager, ToolSpec


class TestInstallCommandGeneration(unittest.TestCase):

    def _manager_with_pm(self, pm_name, which_path):
        with patch("esim_tool_manager.core.shutil.which", return_value=which_path):
            manager = ToolManager()
        manager.platform_info.package_manager = pm_name
        # These tests simulate specific target platforms (apt=Linux, brew=Mac,
        # choco=Windows) regardless of the host OS actually running the suite.
        manager.platform_info.is_windows = (pm_name == "choco")
        return manager
    @patch("esim_tool_manager.core.os.geteuid", return_value=1000, create=True)  # simulate non-root
    @patch("esim_tool_manager.core.shutil.which", return_value="/usr/bin/sudo")
    def test_apt_command_built_correctly_non_root(self, _which, _euid):
        manager = self._manager_with_pm("apt", "/usr/bin/apt")
        spec = ToolSpec(
            name="ngspice", version_check_cmd=["ngspice", "-v"],
            version_regex=r"(\d+)", latest_known_version="42", apt_package="ngspice",
        )
        cmd = manager._build_install_command(spec)
        self.assertEqual(cmd, ["sudo", "apt", "install", "-y", "ngspice"])

    @patch("esim_tool_manager.core.os.geteuid", return_value=0, create=True)  # simulate root
    def test_apt_command_built_correctly_as_root(self, _euid):
        manager = self._manager_with_pm("apt", "/usr/bin/apt")
        spec = ToolSpec(
            name="ngspice", version_check_cmd=["ngspice", "-v"],
            version_regex=r"(\d+)", latest_known_version="42", apt_package="ngspice",
        )
        cmd = manager._build_install_command(spec)
        self.assertEqual(cmd, ["apt", "install", "-y", "ngspice"],
                          "Running as root must not prepend 'sudo'")

    def test_brew_command_built_correctly(self):
        manager = self._manager_with_pm("brew", "/usr/local/bin/brew")
        spec = ToolSpec(
            name="ngspice", version_check_cmd=["ngspice", "-v"],
            version_regex=r"(\d+)", latest_known_version="42", brew_package="ngspice",
        )
        cmd = manager._build_install_command(spec)
        self.assertEqual(cmd, ["brew", "install", "ngspice"])

    def test_choco_command_built_correctly(self):
        manager = self._manager_with_pm("choco", "choco.exe")
        spec = ToolSpec(
            name="ngspice", version_check_cmd=["ngspice", "-v"],
            version_regex=r"(\d+)", latest_known_version="42", choco_package="ngspice",
        )
        cmd = manager._build_install_command(spec)
        self.assertEqual(cmd, ["choco", "install", "ngspice", "-y"])

    def test_no_command_when_package_manager_unsupported(self):
        manager = self._manager_with_pm(None, None)
        spec = ToolSpec(
            name="ngspice", version_check_cmd=["ngspice", "-v"],
            version_regex=r"(\d+)", latest_known_version="42",
        )
        self.assertIsNone(manager._build_install_command(spec))


class TestDependencySeparation(unittest.TestCase):
    """
    Verifies the fix where build-only dependencies (gcc/make) no longer
    block a package-manager install; only true runtime dependencies can.
    """

    @patch("esim_tool_manager.core.shutil.which")
    def test_missing_build_deps_do_not_block_check(self, mock_which):
        # gcc/make missing, but no runtime deps required -> should pass.
        def which_side_effect(binary):
            return None if binary in ("gcc", "make") else f"/usr/bin/{binary}"
        mock_which.side_effect = which_side_effect

        manager = ToolManager()
        ok = manager.check_dependencies("ngspice")
        self.assertTrue(ok, "Build-only dependencies must not block installation")

    @patch("esim_tool_manager.core.shutil.which", return_value=None)
    def test_missing_runtime_deps_block_check(self, _mock_which):
        manager = ToolManager()
        # Inject a fake runtime dependency requirement for this test.
        manager.config.registry["ngspice"]["runtime_dependencies"] = ["some_required_lib"]
        ok = manager.check_dependencies("ngspice")
        self.assertFalse(ok, "Missing runtime dependencies must block installation")


if __name__ == "__main__":
    unittest.main()
