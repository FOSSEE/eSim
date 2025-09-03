import logging, os, pathlib, platform

def _user_log_path():
    if platform.system().lower().startswith("win"):
        root = os.environ.get("APPDATA", str(pathlib.Path.home()))
        d = pathlib.Path(root) / "esim-tool-manager"
    else:
        d = pathlib.Path.home() / ".config" / "esim-tool-manager"
    d.mkdir(parents=True, exist_ok=True)
    return d / "etm.log"

def configure_logging(repo_log_path=None):
    logger = logging.getLogger("etm")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    ulp = _user_log_path()
    fh_user = logging.FileHandler(ulp, encoding="utf-8")
    fh_user.setFormatter(fmt)
    logger.addHandler(fh_user)

    if repo_log_path:
        rp = pathlib.Path(repo_log_path)
        rp.parent.mkdir(parents=True, exist_ok=True)
        fh_repo = logging.FileHandler(rp, encoding="utf-8")
        fh_repo.setFormatter(fmt)
        logger.addHandler(fh_repo)

    return logger
