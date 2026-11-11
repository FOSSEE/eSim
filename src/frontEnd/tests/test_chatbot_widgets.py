"""eSim Copilot chat widgets under eSim 2.6 (PyQt6 and the Aurora theme).

The chatbot was developed on a branch whose main window was still PyQt5,
so several of its code paths had never run under PyQt6 or eSim's theme.
"""
import os
import sys
from unittest.mock import MagicMock

import pytest

_FE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _FE not in sys.path:
    sys.path.insert(0, _FE)


def test_chatbot_thread_imports_without_chromadb(monkeypatch):
    # The chat window does not use documentation retrieval, so a missing
    # chromadb must not stop the chatbot (or eSim) from loading.
    monkeypatch.setitem(sys.modules, "chromadb", None)
    for name in [m for m in sys.modules if m == "chatbot" or m.startswith("chatbot.")]:
        monkeypatch.delitem(sys.modules, name)

    import chatbot.chatbot_thread  # noqa: F401


def test_session_click_reads_session_id_from_item(qapp):
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QListWidgetItem
    from frontEnd.Chatbot import ChatbotGUI

    item = QListWidgetItem("past chat")
    item.setData(Qt.ItemDataRole.UserRole, "session-42")
    gui = MagicMock(_current_session_id="session-42", _viewing_past_session=False)

    # Clicking the session that is already shown is a no-op; reaching that
    # early return proves the session id was read from the item.
    ChatbotGUI._on_session_clicked(gui, item)

    gui._save_current_session.assert_not_called()


@pytest.fixture(params=["style_light.qss", "style_dark.qss"])
def esim_theme(qapp, request):
    """eSim's real theme, whose global QPushButton min-width/padding the
    chatbot's small fixed-size buttons were never designed for."""
    from frontEnd import theme_utils
    qapp.setStyleSheet(theme_utils.build_qss(
        request.param, "dark" in request.param, "default", "system", "system", 100))
    yield
    qapp.setStyleSheet("")


def _buttons_not_at_fixed_size(root):
    from PyQt6.QtWidgets import QPushButton, QWIDGETSIZE_MAX
    root.ensurePolished()  # stylesheets apply at polish, i.e. when shown
    return [(b.text(), b.minimumSize(), b.maximumSize())
            for b in root.findChildren(QPushButton)
            if b.maximumWidth() < QWIDGETSIZE_MAX
            and b.maximumHeight() < QWIDGETSIZE_MAX
            and b.minimumSize() != b.maximumSize()]


def test_chat_panel_stays_a_side_panel_under_esim_theme(esim_theme, monkeypatch):
    from PyQt6 import sip
    from frontEnd.Chatbot import ChatbotGUI

    # No Ollama probing or server start from a unit test.
    monkeypatch.setattr(ChatbotGUI, "_startup_check", lambda self: None)
    monkeypatch.setattr(ChatbotGUI, "_update_ollama_status", lambda self: None)
    gui = ChatbotGUI()
    try:
        assert _buttons_not_at_fixed_size(gui) == []
        assert gui.minimumSizeHint().width() <= 480
    finally:
        gui._status_poll_timer.stop()
        sip.delete(gui)


def test_dynamic_chat_widgets_keep_button_sizes_under_esim_theme(esim_theme, qapp, tmp_path):
    import time
    from PyQt6 import sip
    from PyQt6.QtGui import QColor, QPixmap
    from frontEnd.Chatbot import ChatbotGUI, ChatHistoryViewer, _SessionItemWidget

    image = tmp_path / "schematic.png"
    pix = QPixmap(64, 64)
    pix.fill(QColor("white"))
    pix.save(str(image))

    widgets = [
        _SessionItemWidget("s1", "RC filter", "2026-09-28", msg_count=2),
        ChatHistoryViewer({"title": "RC filter", "messages": []}),
        ChatbotGUI._make_thumbnail(MagicMock(), str(image)),
    ]
    try:
        for widget in widgets:
            assert _buttons_not_at_fixed_size(widget) == [], type(widget).__name__
    finally:
        # ChatHistoryViewer schedules a 120 ms scroll on its browser; let it
        # fire while the widgets are alive, or it lands in a later test.
        end = time.monotonic() + 0.3
        while time.monotonic() < end:
            qapp.processEvents()
        for widget in widgets:
            sip.delete(widget)


def test_image_thumbnail_scales_real_image(qapp, tmp_path):
    from PyQt6.QtGui import QColor, QPixmap
    from PyQt6.QtWidgets import QLabel
    from frontEnd.Chatbot import ChatbotGUI

    image = tmp_path / "schematic.png"
    pix = QPixmap(640, 480)
    pix.fill(QColor("white"))
    assert pix.save(str(image))

    card = ChatbotGUI._make_thumbnail(MagicMock(), str(image))

    thumbs = [lbl.pixmap() for lbl in card.findChildren(QLabel)
              if not lbl.pixmap().isNull()]
    assert thumbs and thumbs[0].width() <= 68 and thumbs[0].height() <= 36


def _debug_error_prompt(monkeypatch, tmp_path, log_text):
    """Run ChatbotGUI.debug_error on a log and return what it asks the model."""
    from frontEnd import Chatbot

    project = tmp_path / "proj"
    project.mkdir()
    log = project / "ngspice_error.log"
    log.write_text(log_text)
    monkeypatch.setattr(
        Chatbot, "Appconfig",
        lambda: MagicMock(current_project={"ProjectName": str(project)}))
    gui = MagicMock()

    Chatbot.ChatbotGUI.debug_error(gui, str(log))

    gui.debug_ollama.assert_called_once()
    return gui.chat_history[-1]


def test_debug_error_keeps_errors_that_come_before_the_banner(monkeypatch, tmp_path):
    prompt = _debug_error_prompt(monkeypatch, tmp_path, (
        "Warning: singular matrix:  check node v1#branch\n"
        "Error: Transient op failed, timestep too small\n"
        "Note: No compatibility mode selected!\n"
        "Circuit: * conflicting sources\n"))

    assert "timestep too small" in prompt
    assert "Circuit:" not in prompt


def test_debug_error_sends_whole_log_when_ngspice_stops_early(monkeypatch, tmp_path):
    # A parse error aborts ngspice before it prints any banner, so the
    # banner-based trimming would otherwise send the model an empty log.
    prompt = _debug_error_prompt(monkeypatch, tmp_path, (
        "Error: unknown subckt: x1 0 c_out v_out lm555n\n"
        "    in line no. 12 from file rc.cir.out\n"
        "    Simulation interrupted due to error!\n"))

    assert "unknown subckt" in prompt
    assert "interrupted due to error" in prompt


def test_debug_error_keeps_errors_after_the_circuit_banner(monkeypatch, tmp_path):
    # eSim's own ngspice (nghdl-simulator) prints the error AFTER "Circuit:"
    # and, having aborted, never prints "Total CPU time"; anything printed
    # before "No compatibility" must not crowd the error out.
    prompt = _debug_error_prompt(monkeypatch, tmp_path, (
        "Warning: Unusual leading characters like ')' in netlist\n"
        "Note: No compatibility mode selected!\n"
        "Circuit: * rc filter\n"
        "Error: unknown subckt: x1 0 c_out v_out lm555n\n"
        "    Simulation interrupted due to error!\n"))

    assert "unknown subckt" in prompt
    assert "Unusual leading characters" in prompt


def test_bordered_session_buttons_keep_their_exact_size(esim_theme):
    # Stylesheet widths exclude the border, so a 1px-bordered 28px button
    # pinned naively renders 30px.
    from frontEnd.Chatbot import _SessionItemWidget

    row = _SessionItemWidget("s1", "RC filter", "2026-09-28", msg_count=2)
    row.ensurePolished()

    assert {(b.minimumSize().width(), b.minimumSize().height())
            for b in (row._rename_btn, row._del_btn)} == {(28, 28)}


def test_chat_window_requires_the_backend_default_text_model():
    # One text model for the whole chatbot. The window used to require
    # qwen2.5-coder:3b while the backend (and the old setup script) used
    # qwen2.5:3b, so users downloaded two 3B models.
    from chatbot import ollama_runner
    from chatbot.chatbot_thread import REQUIRED_MODELS

    assert ollama_runner._DEFAULT_TEXT_MODEL in REQUIRED_MODELS
    assert not any("coder" in m for m in REQUIRED_MODELS)


def test_missing_vision_model_hint_names_the_configured_model(qapp, monkeypatch):
    from frontEnd import Chatbot

    gui = MagicMock()
    monkeypatch.setattr(Chatbot, "_system_bubble", lambda text: text)
    gui._auto_switch_model.return_value = -1   # no vision model installed

    assert Chatbot.ChatbotGUI._warn_or_switch_to_vision_model(gui) is False

    hint = gui.chat_display.append.call_args[0][0]
    assert "ollama pull %s" % Chatbot.VISION_MODEL in hint


def test_status_poll_keeps_a_check_that_is_still_running(monkeypatch):
    # The panel polls Ollama every 5 s. A check that outlives the interval
    # (a sleeping or throttled Mac) used to be replaced while running, and Qt
    # aborts with "QThread: Destroyed while thread is still running".
    from frontEnd import Chatbot

    started = []
    monkeypatch.setattr(Chatbot, "OllamaStatusWorker", lambda: started.append(MagicMock()) or started[-1])
    gui = MagicMock()
    running = gui._status_worker
    running.isRunning.return_value = True

    Chatbot.ChatbotGUI._update_ollama_status(gui)

    assert gui._status_worker is running
    assert started == []


def test_status_poll_starts_a_new_check_once_the_last_one_finished(monkeypatch):
    from frontEnd import Chatbot

    started = []
    monkeypatch.setattr(Chatbot, "OllamaStatusWorker", lambda: started.append(MagicMock()) or started[-1])
    gui = MagicMock()
    gui._status_worker.isRunning.return_value = False

    Chatbot.ChatbotGUI._update_ollama_status(gui)

    assert len(started) == 1
    assert gui._status_worker is started[0]
    started[0].start.assert_called_once_with()
