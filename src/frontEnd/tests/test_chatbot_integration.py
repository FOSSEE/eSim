"""The AI assistant hosted inside the eSim 2.6 main window.

Covers the dock, its View-menu and floating-button toggles, shutdown, and
the project-explorer "Analyze Netlist" entries.
"""
import os
import sys

import pytest

_FE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _FE not in sys.path:
    sys.path.insert(0, _FE)


@pytest.fixture
def build_app(qapp, monkeypatch):
    """Build the real main window with a stand-in for the chat widget.

    The stand-in keeps these tests off the network: the real ChatbotGUI
    probes and may start a local Ollama server when it is constructed.
    """
    from frontEnd import Application as app_module
    built = []

    def build(chat_widget_cls):
        monkeypatch.setattr(app_module, "ChatbotGUI", chat_widget_cls)
        window = app_module.Application()
        built.append(window)
        return window

    yield build
    from PyQt6 import sip
    for window in built:
        if not sip.isdeleted(window):
            window.deleteLater()
    qapp.processEvents()


def _stub_chat_widget():
    from PyQt6.QtWidgets import QWidget

    class StubChat(QWidget):
        closed = False

        def __init__(self):
            super().__init__()
            self.setMinimumSize(420, 340)  # same as the real ChatbotGUI

        def closeEvent(self, event):
            StubChat.closed = True
            super().closeEvent(event)

    return StubChat


def _view_menu_actions(window):
    view = next(a.menu() for a in window.menuBar().actions()
                if a.text() == "&View")
    return view.actions()


def _view_menu_texts(window):
    return [a.text() for a in _view_menu_actions(window)]


def test_app_starts_without_chatbot_packages(build_app):
    window = build_app(None)

    assert window.chatbot_dock is None
    assert "AI Assistant" not in _view_menu_texts(window)
    window.resize(900, 600)  # resize hook must tolerate the missing dock


def test_chatbot_is_docked_on_the_right(build_app):
    from PyQt6.QtCore import Qt

    stub = _stub_chat_widget()
    window = build_app(stub)

    assert isinstance(window.chatbot_dock.widget(), stub)
    assert (window.dockWidgetArea(window.chatbot_dock)
            == Qt.DockWidgetArea.RightDockWidgetArea)


def test_chatbot_opens_as_side_panel_not_half_the_window(build_app, qapp):
    window = build_app(_stub_chat_widget())
    window.resize(1440, 900)
    window.show()
    qapp.processEvents()

    assert 420 <= window.chatbot_dock.width() <= 480
    assert window.centralWidget().width() > window.width() // 2


def test_view_menu_toggles_chatbot(build_app, qapp):
    window = build_app(_stub_chat_widget())
    window.show()
    qapp.processEvents()
    toggle = next(a for a in _view_menu_actions(window)
                  if a.text() == "AI Assistant")

    assert window.chatbot_dock.isVisible()
    toggle.trigger()
    assert not window.chatbot_dock.isVisible()
    toggle.trigger()
    assert window.chatbot_dock.isVisible()


def test_floating_button_toggles_and_sits_beside_dock(build_app, qapp):
    window = build_app(_stub_chat_widget())
    window.resize(1200, 800)
    window.show()
    qapp.processEvents()

    button = window.chatboticon
    assert button.geometry().right() < window.width() - window.chatbot_dock.width()

    window.openChatbot()
    qapp.processEvents()
    assert not window.chatbot_dock.isVisible()
    assert button.geometry().right() < window.width()
    assert button.geometry().right() >= window.width() - button.width() - 20


def test_exit_closes_chatbot(build_app, qapp, monkeypatch):
    from PyQt6.QtWidgets import QMessageBox
    from frontEnd import Application as app_module

    stub = _stub_chat_widget()
    window = build_app(stub)
    window.show()
    monkeypatch.setattr(app_module.Dialogs, "question",
                        lambda *a, **k: QMessageBox.StandardButton.Yes)

    window.close()

    assert stub.closed


def test_destroying_window_raises_no_slot_errors(build_app, qapp, monkeypatch):
    from PyQt6 import sip

    errors = []
    monkeypatch.setattr(sys, "excepthook", lambda *exc: errors.append(exc[1]))
    window = build_app(_stub_chat_widget())
    window.show()
    qapp.processEvents()

    sip.delete(window)
    qapp.processEvents()

    assert errors == []


def _recording_chat_widget():
    base = _stub_chat_widget()

    class RecordingChat(base):
        analysed = []
        debugged = []

        def analyse_netlist(self, path):
            RecordingChat.analysed.append(path)

        def debug_error(self, log):
            RecordingChat.debugged.append(log)

    return RecordingChat


def _chatbot_menu(window, level, path):
    from PyQt6.QtWidgets import QMenu

    menu = QMenu(window)  # parented, so its actions outlive this helper
    window.obj_Mainview.obj_projectExplorer._add_chatbot_actions(menu, level, path)
    return {a.text(): a for a in menu.actions()}


def test_project_menu_sends_project_netlist_to_chatbot(build_app, qapp, tmp_path):
    chat = _recording_chat_widget()
    window = build_app(chat)
    window.show()
    window.chatbot_dock.hide()
    project = tmp_path / "rc_filter"

    actions = _chatbot_menu(window, 0, str(project))
    actions["Analyze Project Netlist"].trigger()

    assert chat.analysed == [str(project / "rc_filter.cir.out")]
    assert window.chatbot_dock.isVisible()


def test_project_netlist_uses_project_file_stem_not_folder_case(build_app, tmp_path):
    # The explorer keys projects by a canonical path, which is lower-cased on
    # case-insensitive filesystems; the netlist is named after the .proj stem.
    chat = _recording_chat_widget()
    window = build_app(chat)
    project = tmp_path / "rc_filter"
    project.mkdir()
    (project / "RC_Filter.proj").write_text("")

    _chatbot_menu(window, 0, str(project))["Analyze Project Netlist"].trigger()

    assert chat.analysed == [str(project / "RC_Filter.cir.out")]


@pytest.mark.parametrize("name, offered", [
    ("rc_filter.cir", True),
    ("rc_filter.cir.out", True),
    ("rc_filter.net", True),
    ("rc_filter.kicad_sch", False),
])
def test_file_menu_offers_netlist_analysis_for_netlists_only(build_app, name, offered):
    chat = _recording_chat_widget()
    window = build_app(chat)

    actions = _chatbot_menu(window, 1, "/proj/" + name)

    assert ("Analyze this Netlist" in actions) is offered
    if offered:
        actions["Analyze this Netlist"].trigger()
        assert chat.analysed[-1] == "/proj/" + name


def test_right_click_on_tree_offers_analysis(build_app, monkeypatch, tmp_path):
    from PyQt6 import QtCore, QtWidgets

    window = build_app(_recording_chat_widget())
    tree = window.obj_Mainview.obj_projectExplorer.treewidget
    project = str(tmp_path / "rc_filter")
    node = QtWidgets.QTreeWidgetItem(tree, ["rc_filter", project])
    child = QtWidgets.QTreeWidgetItem(
        node, ["rc_filter.cir", project + "/rc_filter.cir"])
    shown = []
    monkeypatch.setattr(QtWidgets.QMenu, "exec",
                        lambda menu, *a: shown.append(
                            [act.text() for act in menu.actions()]))

    for item in (node, child):
        tree.setCurrentItem(item)
        window.obj_Mainview.obj_projectExplorer.openMenu(QtCore.QPoint(0, 0))

    assert "Analyze Project Netlist" in shown[0]
    assert "Rename Project" in shown[0]  # master's own entries are kept
    assert "Analyze this Netlist" in shown[1]
    assert "Open" in shown[1]


def test_no_chatbot_menu_entries_without_chatbot(build_app):
    window = build_app(None)

    assert _chatbot_menu(window, 0, "/proj/rc_filter") == {}
    assert _chatbot_menu(window, 1, "/proj/rc_filter.cir") == {}


@pytest.fixture
def failed_project(tmp_path, monkeypatch):
    """A current project whose last ngspice run failed and left its log."""
    from configuration.Appconfig import Appconfig

    project = tmp_path / "rc_filter"
    project.mkdir()
    log = project / "ngspice_error.log"
    log.write_text("Error: unknown subckt: x1\n")
    monkeypatch.setitem(Appconfig.current_project, "ProjectName", str(project))
    return log


def _simulation_ended(window, exit_code):
    from PyQt6 import QtCore
    window.plotSimulationData(QtCore.QProcess.ExitStatus.NormalExit, exit_code)


def test_failed_simulation_is_explained_by_the_assistant(build_app, failed_project):
    chat = _recording_chat_widget()
    window = build_app(chat)
    window.show()
    window.chatbot_dock.hide()

    _simulation_ended(window, exit_code=1)

    assert chat.debugged == [str(failed_project)]
    assert window.chatbot_dock.isVisible()


def test_failure_without_a_log_is_not_sent(build_app, failed_project):
    chat = _recording_chat_widget()
    window = build_app(chat)
    failed_project.unlink()  # e.g. cancelled or abandoned run

    _simulation_ended(window, exit_code=1)

    assert chat.debugged == []


def test_successful_simulation_is_not_sent(build_app, failed_project, monkeypatch):
    chat = _recording_chat_widget()
    window = build_app(chat)
    monkeypatch.setattr(window.obj_Mainview.obj_dockarea, "plottingEditor",
                        lambda: None)

    _simulation_ended(window, exit_code=0)

    assert chat.debugged == []


def test_failed_simulation_without_chatbot(build_app, failed_project):
    window = build_app(None)

    _simulation_ended(window, exit_code=1)  # must not raise


def test_run_abandoned_after_project_closed(build_app, monkeypatch):
    # Closing the project mid-run destroys the simulation dock, which still
    # reports a crashed run; by then there is no current project.
    from PyQt6 import QtCore
    from configuration.Appconfig import Appconfig

    chat = _recording_chat_widget()
    window = build_app(chat)
    monkeypatch.setitem(Appconfig.current_project, "ProjectName", None)

    window.plotSimulationData(QtCore.QProcess.ExitStatus.CrashExit, -1)

    assert chat.debugged == []
