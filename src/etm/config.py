import os, json, pathlib, platform
from typing import Dict, Any

def _config_dir() -> pathlib.Path:
    if platform.system().lower().startswith("win"):
        root = os.environ.get("APPDATA", str(pathlib.Path.home()))
        d = pathlib.Path(root) / "esim-tool-manager"
    else:
        d = pathlib.Path.home() / ".config" / "esim-tool-manager"
    d.mkdir(parents=True, exist_ok=True)
    return d

def config_path() -> pathlib.Path:
    return _config_dir() / "config.json"

def load_config() -> Dict[str, Any]:
    p = config_path()
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    cfg = {
        "esim_root": "",
        "custom_paths": [],
        "preferred_pkgmgr": None,
        "env": {}
    }
    save_config(cfg)
    return cfg

def save_config(cfg: Dict[str, Any]) -> None:
    p = config_path()
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
