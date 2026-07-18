"""
icelang_plugin.runner
=====================
Sole interface between the plugin and the ICELang compiler.

Responsibilities:
- Locate the ICELang compiler root on the filesystem
- Add it to sys.path so compiler modules are importable
- Call main.run(ilang_path, output_dir) and return the output paths
- Raise RunnerError with a human-readable message on any failure

Nothing in this file modifies the compiler. It is a thin adapter.
"""

import os
import sys
import importlib
from pathlib import Path


class RunnerError(Exception):
    pass


def _find_compiler_root() -> Path:
    """
    Locate the ICELang compiler root directory.

    Search order:
    1. Environment variable ICELANG_ROOT if set
    2. Sibling directory of this plugin (../icelang relative to plugin dir)
    3. eSim source tree: ~/eSim/src/icelang/
    4. Common install paths
    """
    env_root = os.environ.get("ICELANG_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root)

    plugin_dir  = Path(__file__).parent
    candidates  = [
        plugin_dir.parent / "icelang",
        Path.home() / "icelang",
        Path.home() / "eSim" / "src" / "icelang",
        Path("/usr/share/esim/icelang"),
    ]

    for c in candidates:
        if (c / "main.py").exists():
            return c

    raise RunnerError(
        "ICELang compiler not found. Set the ICELANG_ROOT environment "
        "variable to the directory containing main.py, or install ICELang "
        "alongside this plugin."
    )


def run(ilang_path: str, output_dir: str) -> dict:
    """
    Compile a .ilang source file to .kicad_sch and .cir.

    Parameters
    ----------
    ilang_path : str
        Absolute path to the .ilang source file.
    output_dir : str
        Directory where output files will be written.

    Returns
    -------
    dict with keys:
        kicad_sch : str  — absolute path to generated .kicad_sch
        spice_cir : str  — absolute path to generated .cir
        circuit_name : str — name of the compiled circuit block

    Raises
    ------
    RunnerError
        If the compiler cannot be found, the source has errors, or
        output generation fails.
    """
    ilang_path = Path(ilang_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not ilang_path.exists():
        raise RunnerError(f"Source file not found: {ilang_path}")

    if not ilang_path.suffix == ".ilang":
        raise RunnerError(f"Expected a .ilang file, got: {ilang_path.name}")

    output_dir.mkdir(parents=True, exist_ok=True)

    compiler_root = _find_compiler_root()

    if str(compiler_root) not in sys.path:
        sys.path.insert(0, str(compiler_root))

    # Force reimport in case a stale version is cached
    for mod in list(sys.modules.keys()):
        if mod in ("main", "icelang_parser", "component_registry",
                   "pin_reader", "graph_builder", "placement_engine",
                   "wire_router", "kicad_gen", "spice_gen"):
            del sys.modules[mod]

    try:
        import main as _compiler_main
    except ImportError as e:
        raise RunnerError(
            f"Failed to import ICELang compiler from {compiler_root}: {e}"
        )

    try:
        result = _compiler_main.run(str(ilang_path), str(output_dir))
    except SystemExit as e:
        raise RunnerError(f"Compiler exited with code {e.code}")
    except Exception as e:
        raise RunnerError(f"Compiler error: {e}")

    circuit_name = ilang_path.stem
    kicad_sch    = output_dir / f"{circuit_name}.kicad_sch"
    spice_cir    = output_dir / f"{circuit_name}.cir"

    if not kicad_sch.exists():
        raise RunnerError(
            f"Compiler completed but {kicad_sch.name} was not produced. "
            "Check compiler output for semantic errors."
        )

    return {
        "kicad_sch":    str(kicad_sch),
        "spice_cir":    str(spice_cir) if spice_cir.exists() else None,
        "circuit_name": circuit_name,
    }
