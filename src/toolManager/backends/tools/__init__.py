from .tools import TOOL_FUNCS

def run(tool_id, cmd, version, backend, upgrade=False):
    funcs = TOOL_FUNCS.get(tool_id)
    if not funcs:
        backend.print_status("not_supported", "none", version); return
    if cmd == "check":
        funcs["check"](version, backend)
    elif cmd in ("install", "update"):
        funcs["install"](version, cmd == "update" or upgrade, backend)
    elif cmd == "uninstall":
        fn = funcs.get("uninstall")
        if fn: fn(version, backend)
        else: backend.print_status("not_supported", "none", "none")
