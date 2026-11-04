"""Shared fixtures for the Tool Manager unit tests.

The backend modules import each other by bare name (``from platform_utils
import ...``) and decide platform-specific behaviour at import time, so the
``fresh_import`` fixture imports a FRESH copy of a module with ``sys.platform``
faked and restores ``sys.modules`` afterwards. Nothing here runs a real
package manager, Chocolatey, MSYS2 or an EDA tool.
"""
import importlib
import sys
from pathlib import Path

# Import the stdlib modules the backends use *before* sys.platform is faked,
# so they initialise for the real host.
import argparse  # noqa: F401
import contextlib  # noqa: F401
import json  # noqa: F401
import threading  # noqa: F401
import urllib.request  # noqa: F401
import zipfile  # noqa: F401

import pytest

TOOLMANAGER_DIR = Path(__file__).resolve().parents[1]

# Modules that must be re-imported together so they see the faked platform.
_BACKEND_MODULES = ("platform_utils", "utils", "tool_manager_linux",
                    "tool_manager_windows")


@pytest.fixture
def fresh_import(monkeypatch):
    """Return fresh_import(module_name, platform) -> freshly imported module."""
    saved = {name: sys.modules.get(name) for name in _BACKEND_MODULES}
    monkeypatch.syspath_prepend(str(TOOLMANAGER_DIR))

    def _import(name, plat):
        for mod in _BACKEND_MODULES:
            sys.modules.pop(mod, None)
        # Fake the platform only while importing: the modules record it in
        # IS_WINDOWS & co. at import time, and pytest itself (tmp_path, ...)
        # must keep seeing the real host afterwards.
        with monkeypatch.context() as m:
            m.setattr(sys, "platform", plat)
            # tool_manager_windows creates its Download/ folder at import
            # time; keep the source tree untouched while testing.
            m.setattr(Path, "mkdir", lambda self, *a, **kw: None)
            return importlib.import_module(name)

    yield _import

    for name, mod in saved.items():
        if mod is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = mod
