import os, shutil, subprocess, threading
from pathlib import Path
from typing import Optional
from ..base import Backend
from . import file_ops as _file_ops, pm as _pm, search as _search
from pm_platform import detect_package_manager

_BASH_LOCK = threading.Lock()

class LinuxBackend(Backend):
    name = "linux"

    def __init__(self, base_dir: Optional[Path] = None):
        super().__init__()
        self._base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self._download_dir = self._base_dir / "Download"
        self._download_dir.mkdir(parents=True, exist_ok=True)
        self._pm_name: Optional[str] = detect_package_manager()

    def which(self, cmd):
        return shutil.which(cmd)

    def print_status(self, state, installed, target):
        if installed: installed = str(installed).strip().replace("\n","").replace("\r","")
        print(f"{state}|{installed}|{target}", flush=True)

    def _search_fn(self, tool_id, version):
        _S = {
            "kicad": lambda: _search.find_kicad(version, self.run_cmd, self.which),
            "ngspice": lambda: _search.find_ngspice(version, self.run_cmd, self.which),
            "ghdl": lambda: _search.find_ghdl(version, self.run_cmd, self.which),
            "verilator": lambda: _search.find_verilator(version, self.run_cmd, self.which),
            "llvm": lambda: _search.find_llvm(version, self.run_cmd, self.which),
            "esim": lambda: _search.find_tool("esim", version, self.run_cmd, self.which),
            "chocolatey": lambda: (None, None),
            "pyqt": lambda: self._find_pyqt(version),
        }
        return _S.get(tool_id)

    def _find_pyqt(self, version):
        result = self.run_cmd([os.sys.executable, "-c", "import PyQt6.QtCore; print(PyQt6.QtCore.PYQT_VERSION_STR)"], timeout=10)
        if result and result.returncode == 0:
            ver = (result.stdout or "").strip()
            return ("PyQt6", ver) if ver else (None, None)
        return (None, None)

    def find_executable(self, tool_id, version):
        fn = self._search_fn(tool_id, version)
        return fn()[0] if fn else None

    def find_executable_with_version(self, tool_id, version):
        fn = self._search_fn(tool_id, version)
        return fn() if fn else (None, None)

    def get_tool_version(self, exe_path):
        try:
            result = self.run_cmd([exe_path, "--version"])
            if result and result.returncode == 0:
                parts = (result.stdout or "").split("\n")[0].strip().split()
                return parts[-1] if parts else None
        except: pass
        return None

    def install_package(self, package, version, fallback_versions=None):
        if not self._pm_name: self.print_status("not_supported", "none", version); return False
        versions = [version] + (fallback_versions or [])
        for v in versions:
            if v == "latest":
                if _pm.pm_install(self._pm_name, package, self.run_cmd): return True
            else:
                spec = f"{package}={v}" if self._pm_name == "apt" else package
                if _pm.pm_install(self._pm_name, spec if self._pm_name != "pacman" else package, self.run_cmd): return True
        return False

    def uninstall_package(self, package, version):
        if not self._pm_name: self.print_status("not_supported", "none", version); return False
        return _pm.pm_uninstall(self._pm_name, package, self.run_cmd)

    def download_file(self, url, filename):
        result = _file_ops.download_file(url, filename, self._download_dir)
        if result is None: raise RuntimeError(f"Download failed: {url}")
        return result

    def extract_zip(self, archive, dest_dir): return _file_ops.extract_zip(archive, dest_dir)
    def extract_7z(self, archive, dest_dir): return _file_ops.extract_7z(archive, dest_dir, run_cmd=self.run_cmd)
    def run_installer(self, exe_path, *args): return _file_ops.run_installer(exe_path, list(args), run_cmd=self.run_cmd)

    def sudo_is_cached(self):
        result = self.run_cmd(["sudo", "-n", "true"])
        return result is not None and result.returncode == 0

    def ensure_sudo(self, password):
        try:
            proc = subprocess.Popen(["sudo","-S","-v"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            proc.communicate(input=password + "\n", timeout=10)
            return proc.returncode == 0
        except: return False

    def clean_package_locks(self):
        locks = {"apt": ["/var/lib/dpkg/lock-frontend","/var/lib/dpkg/lock","/var/cache/apt/archives/lock"],
                 "pacman": ["/var/lib/pacman/db.lck"],"dnf": ["/var/run/yum.pid"],"zypper": ["/var/run/zypp.pid"]}.get(self._pm_name, [])
        for lock in locks:
            self.run_cmd(f"sudo lsof {lock} 2>/dev/null || sudo rm -f {lock}".split(), timeout=10)

    def run_bash_script(self, script_path, *args, cwd=None):
        with _BASH_LOCK:
            self.clean_package_locks()
            script = Path(script_path)
            if not script.is_absolute(): script = self._base_dir / script_path
            if not script.exists(): self.print_status("missing_script", "none", script_path); return False
            rc, _ = self.run_stream(["bash", str(script)] + list(args), timeout=900, cwd=cwd or self._base_dir)
            if rc != 0: self.print_status("script_failed", str(rc), script_path)
            return rc == 0

    @property
    def base_dir(self) -> Path: return self._base_dir

    @property
    def download_dir(self) -> Path: return self._download_dir
