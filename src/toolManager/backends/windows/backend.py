import io, os, platform, shutil, subprocess, sys
from pathlib import Path
from typing import Optional
from ..base import Backend
from . import choco as _choco, file_ops as _file_ops, search as _search

class WindowsBackend(Backend):
    name = "win32"

    def __init__(self, base_dir=None, msys2_path=None):
        super().__init__()
        self._base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self._download_dir = self._base_dir / "Download"
        self._download_dir.mkdir(parents=True, exist_ok=True)
        self._msys2_path = msys2_path or Path(r"C:\msys64")
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')
        from registry import WIN_KICAD_PATHS, WIN_NGSPICE_PATHS, WIN_LLVM_PATHS
        self._win_kicad_paths = WIN_KICAD_PATHS
        self._win_ngspice_paths = WIN_NGSPICE_PATHS
        self._win_llvm_paths = WIN_LLVM_PATHS

    def run_cmd(self, cmd, timeout=30, cwd=None, env=None):
        try:
            startupinfo, cf = (subprocess.STARTUPINFO(), 0)
            if platform.system() == "Windows":
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                cf = subprocess.CREATE_NO_WINDOW
            return subprocess.run(cmd, capture_output=True, text=True, shell=False, timeout=timeout,
                startupinfo=startupinfo, creationflags=cf, encoding='utf-8', errors='ignore', cwd=cwd, env=env)
        except: return None

    def which(self, cmd):
        return shutil.which(cmd)

    def print_status(self, state, installed, target):
        if installed: installed = str(installed).strip().replace('\n','').replace('\r','')
        print(f"{state}|{installed}|{target}", flush=True)

    def _search_fn(self, tool_id, version):
        _S = {
            "chocolatey": lambda: _search.find_chocolatey(version, self.which, self.run_cmd),
            "kicad": lambda: _search.find_kicad(version, self.which, self.run_cmd, self._win_kicad_paths),
            "ngspice": lambda: _search.find_ngspice(version, self.which, self.run_cmd, self._win_ngspice_paths, lambda p: _choco.choco_list(p, self.run_cmd)),
            "llvm": lambda: _search.find_llvm(version, self.which, self.run_cmd, self._win_llvm_paths),
            "ghdl": lambda: _search.find_ghdl(version, self.which, self.run_cmd, self._base_dir, self.msys2_mingw_bin, self._msys2_env()),
            "verilator": lambda: _search.find_verilator(version, self.which, self.run_cmd, self.msys2_mingw_bin, self._msys2_env()),
            "pyqt": lambda: _search.find_pyqt(version, self.run_cmd),
        }
        return _S.get(tool_id)

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
                parts = result.stdout.split("\n")[0].strip().split()
                return parts[-1] if parts else None
        except: pass
        return None

    def install_package(self, package, version, fallback_versions=None):
        from registry import NGSPICE_VERSIONS, LLVM_VERSIONS, KICAD_VERSIONS
        if version == "latest": return _choco.choco_install(package, version, self.run_cmd)
        versions = [version] + (fallback_versions or [])
        for v in versions:
            if _choco.choco_install(package, v, self.run_cmd): return True
        return False

    def uninstall_package(self, package, version):
        return _choco.choco_uninstall(package, version, self.run_cmd)

    def download_file(self, url, filename):
        result = _file_ops.download_file(url, filename, self._download_dir)
        if result is None: raise RuntimeError(f"Download failed: {url}")
        return result

    def extract_zip(self, archive, dest_dir): return _file_ops.extract_zip(archive, dest_dir)
    def extract_7z(self, archive, dest_dir): return _file_ops.extract_7z(archive, dest_dir, run_cmd=self.run_cmd)
    def run_installer(self, exe_path, *args): return _file_ops.run_installer(exe_path, list(args), self.run_cmd)

    @property
    def base_dir(self): return self._base_dir

    @property
    def download_dir(self): return self._download_dir

    @property
    def msys2_bash(self):
        bash = self._msys2_path / "usr" / "bin" / "bash.exe"
        return bash if bash.exists() else None

    @property
    def msys2_mingw_bin(self):
        for c in [self._msys2_path / "mingw64" / "bin", Path(r"C:\FOSSEE\MSYS\mingw64") / "bin"]:
            if c.exists(): return c
        return None

    @property
    def msys2_mingw_root(self):
        for c in [self._msys2_path / "mingw64", Path(r"C:\FOSSEE\MSYS\mingw64")]:
            if c.exists(): return c
        return None

    def _msys2_env(self):
        env = os.environ.copy()
        paths = []
        msys_bin = self.msys2_mingw_bin
        if msys_bin: paths.append(str(msys_bin))
        msys_root = self.msys2_mingw_root
        if msys_root:
            usr_bin = msys_root.parent / "usr" / "bin"
            if usr_bin.exists(): paths.append(str(usr_bin))
        if paths: env["PATH"] = os.pathsep.join(paths) + os.pathsep + env.get("PATH", "")
        return env

    def install_kicad_direct(self, target_version):
        from registry import TOOLS
        spec = TOOLS.get("kicad")
        if not spec: return False
        url = spec.get_download_url(target_version)
        if not url: self.print_status("not_supported", "none", target_version); return False
        exe_path = self.download_file(url, f"kicad-{target_version}.exe")
        return bool(exe_path and self.run_installer(str(exe_path), "/SILENT"))
