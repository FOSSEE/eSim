#!/usr/bin/env python3
"""Capture eSim 2.5 with a real example project loaded.

eSim's main window is the genuine Application() widget tree. We drive it the
same way a user does - through the OpenProjectInfo body() code path is a file
dialog, so instead we populate the project explorer and workspace directly
from a shipped example, which is what opening the project produces.

Rendering uses Qt's offscreen platform (WSLg's Weston refuses X_GetImage).
"""
import os
import sys
import traceback

frontend, outdir, pkg = sys.argv[1], sys.argv[2], sys.argv[3]
os.chdir(frontend)
sys.path.insert(0, frontend)
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.makedirs(outdir, exist_ok=True)

from PyQt5 import QtCore, QtWidgets  # noqa: E402
import Application  # noqa: E402


def settle(ms=2500):
    QtWidgets.QApplication.processEvents()
    QtCore.QThread.msleep(ms)
    QtWidgets.QApplication.processEvents()


def shot(widget, name):
    widget.show()
    settle()
    pix = widget.grab()
    pix.save(os.path.join(outdir, name), "PNG")
    print(f"  {name}: {pix.width()}x{pix.height()}")
    return pix


def force_size(win, w, h):
    """Bypass the layout's size hint with an explicit geometry."""
    win.setMinimumSize(QtCore.QSize(w, h))
    win.resize(w, h)
    win.setGeometry(0, 0, w, h)
    settle()


def main():
    app = QtWidgets.QApplication(sys.argv[:1])
    app.setApplicationName("eSim")

    win = Application.Application()
    win.setWindowTitle("eSim 2.5 - Ubuntu 25.04")
    force_size(win, 1400, 900)
    shot(win, "01-esim-main-window.png")

    # Load a shipped example into the project explorer the way opening a
    # project does: eSim's Appconfig holds project_explorer as dir -> files.
    example = os.path.join(pkg, "Examples", "Astable555")
    cfg = getattr(win, "obj_Appconfig", None) or getattr(win, "appconfig", None)
    loaded = False
    if cfg is not None and hasattr(cfg, "project_explorer"):
        try:
            files = sorted(os.listdir(example))
            cfg.project_explorer[example] = files
            if hasattr(cfg, "print_info"):
                cfg.print_info("Current Project is " + example)
            loaded = True
        except Exception as exc:
            print("  could not populate explorer:", exc)

    # The Workspace pane is what shows the schematic/analysis tabs.
    ws = getattr(win, "obj_workspace", None) or getattr(win, "workspace", None)
    if ws is not None and hasattr(ws, "show"):
        try:
            ws.show()
        except Exception:
            pass

    settle(1500)
    shot(win, "02-esim-with-project.png")

    # Readable crop of the left rail + explorer at native scale.
    for attr in ("obj_projectexplorer", "obj_dockarea"):
        w = getattr(win, attr, None)
        if isinstance(w, QtWidgets.QWidget) and w.isVisible():
            shot(w, f"03-esim-{attr}.png")

    print("done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
