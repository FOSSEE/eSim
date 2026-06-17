"""
backends/tools/__init__.py — Dispatch hub for tool operations.

Each tool module exports ``check(version, backend)``,
``install(version, upgrade, backend)``, and ``uninstall(version, backend)``.
This module maps tool IDs to modules and provides a single ``run()`` entry
point for the CLI adapters.
"""

from . import chocolatey, esim, kicad, ngspice, llvm, ghdl, verilator

_TOOL_MODULES = {
    "chocolatey": chocolatey,
    "esim": esim,
    "kicad": kicad,
    "ngspice": ngspice,
    "llvm": llvm,
    "ghdl": ghdl,
    "verilator": verilator,
}


def run(tool_id: str, cmd: str, version: str,
        backend, upgrade: bool = False) -> None:
    """Dispatch one tool command.

    Parameters
    ----------
    tool_id : str
        One of the keys in ``_TOOL_MODULES``.
    cmd : str
        ``"check"``, ``"install"``, ``"update"``, or ``"uninstall"``.
    version : str
        Target version string.
    backend : Backend
        Platform backend instance.
    upgrade : bool
        If True and *cmd* is ``"update"`` or ``"install"``, upgrade
        instead of fresh-install.
    """
    mod = _TOOL_MODULES.get(tool_id)
    if mod is None:
        backend.print_status("not_supported", "none", version)
        return

    if cmd == "check":
        mod.check(version, backend)
    elif cmd == "install":
        mod.install(version, upgrade, backend)
    elif cmd == "update":
        mod.install(version, True, backend)
    elif cmd == "uninstall":
        if hasattr(mod, "uninstall"):
            mod.uninstall(version, backend)
        else:
            backend.print_status("not_supported", "none", "none")
