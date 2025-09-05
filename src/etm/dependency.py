from . import os_ops

def check_basics():
    findings = {}
    pm = os_ops.pkg_manager()
    if not pm:
        findings["package_manager"] = "NOT FOUND — " + os_ops.suggest_pkgmgr_install()
    else:
        findings["package_manager"] = f"OK ({pm})"

    for util in ["git","curl","python3"]:
        findings[util] = "OK" if os_ops.which(util) else "NOT FOUND"

    return findings
