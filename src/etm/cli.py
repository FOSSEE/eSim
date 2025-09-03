import argparse, sys, pathlib, shlex
from typing import List
from .logging_conf import configure_logging
from . import os_ops
from .tools import list_tool_names, get_tool
from . import config as cfgmod
from . import dependency as dep

REPO_LOG = pathlib.Path(__file__).resolve().parents[2] / "logs" / "etm.log"
log = configure_logging(repo_log_path=REPO_LOG)

def _pm_key():
    osid = os_ops.current_os()
    pm = os_ops.pkg_manager()
    if osid == "linux" and pm == "apt":
        return "linux-apt"
    if osid == "mac" and pm == "brew":
        return "mac-brew"
    if osid == "windows" and pm == "choco":
        return "win-choco"
    return ""

def cmd_list_tools(_args):
    print("\n".join(list_tool_names()))

def cmd_status(args):
    names = args.tools or list_tool_names()
    for name in names:
        tool = get_tool(name)
        if not tool:
            print(f"{name}: unknown tool")
            continue
        rc, out, err = os_ops.run_cmd(tool.check_cmd)
        if rc == 0:
            v = out.splitlines()[0] if out else "version: unknown"
            print(f"{tool.name}: INSTALLED — {v}")
        else:
            print(f"{tool.name}: NOT INSTALLED ({err or 'command failed'})")

def _run_pkgmgr(cmd: List[str]):
    pm = os_ops.pkg_manager()
    if not pm:
        print(os_ops.suggest_pkgmgr_install())
        sys.exit(1)

    full = cmd
    if pm == "apt" and cmd and cmd[0] == "apt-get":
        os_ops.run_cmd(os_ops.prefix_sudo(["apt-get","update"]))

    if pm in ("apt","brew"):
        full = os_ops.prefix_sudo(cmd)

    log.info("Running: %s", " ".join(shlex.quote(x) for x in full))
    rc, out, err = os_ops.run_cmd(full)
    print(out)
    if rc != 0:
        print(err, file=sys.stderr)
    return rc

def cmd_install(args):
    key = _pm_key()
    if not key:
        print(os_ops.suggest_pkgmgr_install())
        sys.exit(1)

    names = args.tools or list_tool_names()
    for name in names:
        tool = get_tool(name)
        if not tool:
            print(f"{name}: unknown tool")
            continue
        cmd = tool.installers.get(key, [])
        if not cmd:
            print(f"{name}: installer not defined for this OS/PM")
            continue
        rc = _run_pkgmgr(cmd)
        print(f"{name}: install {'OK' if rc==0 else 'FAILED'}")

def cmd_update(args):
    key = _pm_key()
    if not key:
        print(os_ops.suggest_pkgmgr_install())
        sys.exit(1)

    names = args.tools or list_tool_names()
    for name in names:
        tool = get_tool(name)
        if not tool:
            print(f"{name}: unknown tool")
            continue
        cmd = tool.updaters.get(key, [])
        if not cmd:
            print(f"{name}: updater not defined for this OS/PM")
            continue
        rc = _run_pkgmgr(cmd)
        print(f"{name}: update {'OK' if rc==0 else 'FAILED'}")

def cmd_configure(args):
    cfg = cfgmod.load_config()
    env = cfg.get("env", {})
    if cfg.get("esim_root"):
        env.setdefault("ESIM_HOME", cfg["esim_root"])
    cfg["env"] = env
    cfgmod.save_config(cfg)

    snippet = []
    for p in cfg.get("custom_paths", []):
        snippet.append(f'export PATH="{p}:$PATH"')
    if snippet:
        print("# Add the following lines to your shell profile (~/.bashrc, ~/.zshrc):")
        print("\n".join(snippet))
    print("Configuration saved to:", cfgmod.config_path())

def cmd_show_config(_args):
    print(cfgmod.config_path().read_text(encoding="utf-8"))

def cmd_set_config(args):
    cfg = cfgmod.load_config()
    cfg[args.key] = args.value
    cfgmod.save_config(cfg)
    print("Updated", args.key, "→", args.value)

def cmd_doctor(_args):
    findings = dep.check_basics()
    for k, v in findings.items():
        print(f"{k}: {v}")

def build_parser():
    p = argparse.ArgumentParser(prog="etm", description="eSim Tool Manager (prototype)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-tools").set_defaults(func=cmd_list_tools)

    st = sub.add_parser("status")
    st.add_argument("tools", nargs="*")
    st.set_defaults(func=cmd_status)

    ins = sub.add_parser("install")
    ins.add_argument("tools", nargs="*")
    ins.set_defaults(func=cmd_install)

    upd = sub.add_parser("update")
    upd.add_argument("tools", nargs="*")
    upd.set_defaults(func=cmd_update)

    cfgp = sub.add_parser("configure")
    cfgp.set_defaults(func=cmd_configure)

    sc = sub.add_parser("show-config")
    sc.set_defaults(func=cmd_show_config)

    setc = sub.add_parser("set-config")
    setc.add_argument("--key", required=True)
    setc.add_argument("--value", required=True)
    setc.set_defaults(func=cmd_set_config)

    doc = sub.add_parser("doctor")
    doc.set_defaults(func=cmd_doctor)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
