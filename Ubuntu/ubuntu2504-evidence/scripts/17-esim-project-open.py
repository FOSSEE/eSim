#!/usr/bin/env python3
"""Capture eSim 2.5 with a shipped example project loaded into the explorer.

Application.open_project() calls OpenProjectInfo.body() (a file dialog) and
then Mainview.obj_projectExplorer.addTreeNode(directory, filelist). We call
addTreeNode with the same arguments the dialog would return, so the UI state
is identical to a user having opened the project - only the dialog is skipped.
"""
import os
import sys
import traceback

frontend, outdir, pkg = sys.argv[1], sys.argv[2], sys.argv[3]
example = os.path.join(pkg, "Examples", "Astable555")
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


def shot(w, name):
    w.show(); settle()
    p = w.grab(); p.save(os.path.join(outdir, name), "PNG")
    print(f"  {name}: {p.width()}x{p.height()}")


def main():
    app = QtWidgets.QApplication(sys.argv[:1])
    win = Application.Application()
    win.setWindowTitle("eSim 2.5 - Ubuntu 25.04")
    settle()

    explorer = win.obj_Mainview.obj_projectExplorer
    filelist = sorted(os.listdir(example))
    print(f"=== loading project {example} ({len(filelist)} files) into the tree")
    explorer.addTreeNode(example, filelist)
    settle()

    shot(win, "05-esim-project-loaded.png")

    # The explorer tree on its own, at native resolution, is the readable view
    # of what eSim shows for an opened project.
    shot(explorer, "06-esim-project-explorer.png")

    print("done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
