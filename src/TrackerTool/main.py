import sys
import csv
import socket
import requests
import csv
import re
# -------- Helpers --------
import getpass
import os
import getpass
from dotenv import load_dotenv
load_dotenv()

from collections import defaultdict
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QComboBox, QFileDialog, QApplication
)
from getmac import get_mac_address

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QMessageBox, QFileDialog, QInputDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QListWidget, QTextEdit, QComboBox, QScrollArea, QFrame, QStackedWidget,
    QDialogButtonBox, QDateEdit,QLineEdit
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# ✅ EXACTLY SAME as your original (no backend/API changes)
#API_BASE_URL = "https://tooltracker-afxj.onrender.com"
API_BASE_URL = os.getenv("API_BASE_URL", "https://tool-tracker-esim-api.onrender.com").rstrip("/")


# -----------------------------
# Modern styling (QSS)
# -----------------------------
APP_QSS = """
QWidget {
    background: #0b1220;
    color: #e5e7eb;
    font-family: "Segoe UI";
    font-size: 12pt;
}

#Shell {
    background: #0b1220;
}

#Sidebar {
    background: #0a1020;
    border-right: 1px solid rgba(255,255,255,0.06);
}

#BrandTitle {
    font-size: 15pt;
    font-weight: 700;
}
#BrandSub {
    color: #9ca3af;
    font-size: 10pt;
}

QPushButton {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 10px 12px;
    background: rgba(255,255,255,0.06);
    color: #e5e7eb;
    font-weight: 600;
}

QPushButton:hover {
    background: rgba(255,255,255,0.10);
    border-color: rgba(255,255,255,0.16);
}

QPushButton:pressed {
    background: rgba(255,255,255,0.12);
}

QPushButton#Primary {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #6366f1, stop:1 #0ea5e9);
    border: none;
}

QPushButton#Danger {
    background: rgba(239, 68, 68, 0.18);
    border: 1px solid rgba(239, 68, 68, 0.35);
}

QPushButton#NavActive {
    background: rgba(99, 102, 241, 0.18);
    border: 1px solid rgba(99, 102, 241, 0.35);
}

QFrame#Card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
}

QLabel#H1 {
    font-size: 16pt;
    font-weight: 800;
}

QLabel#Muted {
    color: #9ca3af;
}

QTableWidget {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    gridline-color: rgba(255,255,255,0.10);
}

QHeaderView::section {
    background: rgba(255,255,255,0.06);
    border: none;
    padding: 8px;
    font-weight: 700;
}

QComboBox, QTextEdit {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 8px 10px;
}

QScrollArea {
    border: none;
    background: transparent;
}
"""


# -----------------------------
# Worker for non-blocking API calls (UI improvement only)
# -----------------------------
class ApiWorker(QThread):
    finished = pyqtSignal(object, object)  # (result, error)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            res = self.fn(*self.args, **self.kwargs)
            self.finished.emit(res, None)
        except Exception as e:
            self.finished.emit(None, e)


# -----------------------------
# Main App
# -----------------------------
class TrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Shell")
        self.setWindowTitle("eSim Tool Tracker")
        self.setMinimumSize(1050, 650)

        # --- Root Layout ---
        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        sb = QVBoxLayout(self.sidebar)
        sb.setContentsMargins(14, 14, 14, 14)
        sb.setSpacing(10)

        # Brand section
        brand = QFrame()
        b = QVBoxLayout(brand)
        b.setContentsMargins(0, 0, 0, 0)
        title = QLabel("eSim Tool Tracker")
        title.setObjectName("BrandTitle")
        sub = QLabel("FOSSEE • eSim Activity Tracker")
        sub.setObjectName("BrandSub")
        b.addWidget(title)
        b.addWidget(sub)
        sb.addWidget(brand)
        sb.addSpacing(10)

        # --- Content stack ---
        self.stack = QStackedWidget()

        # Create pages
        self.page_stats = self.build_stats_page()
        self.page_activity = self.build_activity_page()
        self.page_logs = self.build_logs_page()

        # NEW: Crashes page
        self.page_crashes = self.build_crashes_page()

        self.page_tasks = self.build_tasks_page()
        self.page_releases = self.build_releases_page()
        

        # Add pages to stack (order matters)
        self.stack.addWidget(self.page_stats)         # index 0
        self.stack.addWidget(self.page_activity)      # index 1
        self.stack.addWidget(self.page_logs)          # index 2
        self.stack.addWidget(self.page_crashes)       # index 3  <-- NEW
        self.stack.addWidget(self.page_tasks)         # index 4
        self.stack.addWidget(self.page_releases)      # index 5
        
        # --- Navigation Buttons ---
        self.btn_stats = QPushButton("Statistics")
        self.btn_activity = QPushButton("User Activity")
        self.btn_logs = QPushButton("Logs")

        # NEW: Crashes button
        self.btn_crashes = QPushButton("Crashes")

        self.btn_tasks = QPushButton("Tasks")
        self.btn_releases = QPushButton("Releases")
        # self.btn_builds = QPushButton("Builds / Installers")
        # self.btn_qa = QPushButton("QA / Testing")
        # self.btn_deps = QPushButton("Dependencies")
        # self.btn_docs = QPushButton("Documentation")

        self.btn_quit = QPushButton("Quit")
        self.btn_quit.setObjectName("Danger")

        # Connect buttons
        self.btn_stats.clicked.connect(lambda: self.set_page(0))
        self.btn_activity.clicked.connect(lambda: self.set_page(1))
        self.btn_logs.clicked.connect(lambda: self.set_page(2))
        self.btn_crashes.clicked.connect(lambda: self.set_page(3))   # NEW
        self.btn_tasks.clicked.connect(lambda: self.set_page(4))
        self.btn_releases.clicked.connect(lambda: self.set_page(5))
        # self.btn_builds.clicked.connect(lambda: self.set_page(6))
        # self.btn_qa.clicked.connect(lambda: self.set_page(7))
        # self.btn_deps.clicked.connect(lambda: self.set_page(8))
        # self.btn_docs.clicked.connect(lambda: self.set_page(9))
        self.btn_quit.clicked.connect(self.close)

        # Add buttons to sidebar (clean order)
        sb.addWidget(self.btn_stats)
        sb.addWidget(self.btn_activity)
        sb.addWidget(self.btn_logs)
        sb.addWidget(self.btn_crashes)  # NEW

        sb.addSpacing(10)
        sb.addWidget(self.btn_tasks)
        sb.addWidget(self.btn_releases)
        # sb.addWidget(self.btn_builds)
        # sb.addWidget(self.btn_qa)
        # sb.addWidget(self.btn_deps)
        # sb.addWidget(self.btn_docs)

        sb.addStretch(1)
        sb.addWidget(self.btn_quit)

        # --- Add sidebar and stack to root layout ---
        root.addWidget(self.sidebar)
        root.addWidget(self.stack)

        # Optional: cache holders for crashes page
        self._crashes_cache = []
        self._last_crash_id_seen = 0

        # Set initial page
        self.set_page(0)

    @staticmethod
    def generate_username():
        pc_name = socket.gethostname()
        mac_address = get_mac_address()
        if not mac_address:
            raise Exception("Unable to retrieve MAC address")

        # ✅ test override (same idea as tracker.py)
        forced = os.getenv("SET_USERNAME", "").strip()
        if forced:
            return f"{pc_name}_{forced}_{mac_address.replace(':', '_')}"

        # ✅ default = real windows username (MATCH tracker.py)
        win_user = getpass.getuser()
        return f"{pc_name}_{win_user}_{mac_address.replace(':', '_')}"



    def set_page(self, idx: int):
 
        self.stack.setCurrentIndex(idx)

        # Updated nav order to match NEW indices:
        # 0 Stats, 1 Activity, 2 Logs, 3 Crashes, 4 Tasks, 5 Releases, ...
        nav_buttons = [
            self.btn_stats,
            self.btn_activity,
            self.btn_logs,
            self.btn_crashes,     # NEW
            self.btn_tasks,
            self.btn_releases,
            # self.btn_builds,
            # self.btn_qa, self.btn_deps, self.btn_docs
        ]

        for i, btn in enumerate(nav_buttons):
            btn.setObjectName("NavActive" if i == idx else "")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if idx == 0:
            self.refresh_stats()
        elif idx == 2:
            self.refresh_logs()
        elif idx == 3:            # NEW
            self.refresh_crashes()
        elif idx == 4:
            self.refresh_tasks()
        elif idx == 5:
            self.refresh_releases()
       

    def card(self, title_text: str, subtitle_text: str = ""):
        frame = QFrame()
        frame.setObjectName("Card")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        t = QLabel(title_text)
        t.setObjectName("H1")
        lay.addWidget(t)

        if subtitle_text:
            st = QLabel(subtitle_text)
            st.setObjectName("Muted")
            lay.addWidget(st)

        return frame, lay

    # -------- API calls (same endpoints) --------
    def api_get_stats(self, user_id: str):
        r = requests.get(f"{API_BASE_URL}/statstics", params={"user": user_id}, timeout=10)
        r.raise_for_status()
        return r.json()

    def api_get_sessions(self, user_id: str):
        r = requests.get(f"{API_BASE_URL}/sessions", params={"user": user_id}, timeout=10)
        r.raise_for_status()
        return r.json()

    def api_get_logs(self, user_id: str):
        r = requests.get(f"{API_BASE_URL}/logs", params={"user": user_id}, timeout=10)
        r.raise_for_status()
        return r.json()

    # -------- Pages --------
    def build_stats_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        frame, lay = self.card("Statistics", "Sessions and time tracked for this machine/user.")
        layout.addWidget(frame)

        mrow = QHBoxLayout()
        mrow.setSpacing(12)

        self.lbl_total_hours = QLabel("Total Hours: —")
        self.lbl_avg = QLabel("Avg / Session: —")
        self.lbl_sessions = QLabel("Sessions: —")
        for w in [self.lbl_total_hours, self.lbl_avg, self.lbl_sessions]:
            w.setObjectName("Muted")

        mrow.addWidget(self.lbl_total_hours)
        mrow.addWidget(self.lbl_avg)
        mrow.addWidget(self.lbl_sessions)
        mrow.addStretch(1)
        lay.addLayout(mrow)

        self.table_sessions = QTableWidget()
        self.table_sessions.setColumnCount(5)
        self.table_sessions.setHorizontalHeaderLabels(["User", "Start Time", "End Time", "Duration", "Location"])
        self.table_sessions.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_sessions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        lay.addWidget(self.table_sessions)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setObjectName("Primary")
        self.btn_export.clicked.connect(self.export_data)

        self.btn_delete = QPushButton("Delete a Session…")
        self.btn_delete.setObjectName("Danger")
        self.btn_delete.clicked.connect(self.delete_data)

        actions.addWidget(self.btn_export)
        actions.addWidget(self.btn_delete)
        actions.addStretch(1)
        lay.addLayout(actions)

        return page

    def build_activity_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        frame, lay = self.card("User Activity", "Visualize your sessions as bar / pie / line charts.")
        layout.addWidget(frame)

        row = QHBoxLayout()
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Bar Chart", "Pie Chart", "Line Chart"])
        row.addWidget(QLabel("Chart type:"))
        row.addWidget(self.chart_type)
        row.addStretch(1)

        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setObjectName("Primary")
        self.btn_generate.clicked.connect(self.generate_chart_async)
        row.addWidget(self.btn_generate)
        lay.addLayout(row)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        lay.addWidget(self.scroll_area)

        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_layout.setSpacing(10)
        self.scroll_area.setWidget(self.chart_container)

        return page

    def build_logs_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        frame, lay = self.card("Logs", "Shows logs stored in the backend for this user.")
        layout.addWidget(frame)

        self.log_list = QListWidget()
        lay.addWidget(self.log_list)

        self.btn_view_log = QPushButton("View Selected Log")
        self.btn_view_log.setObjectName("Primary")
        self.btn_view_log.clicked.connect(self.view_selected_log)
        lay.addWidget(self.btn_view_log)

        self._logs_cache = []
        return page

    # -------- Stats (async refresh) --------
    def refresh_stats(self):
        user = self.generate_username()
        print("GUI user_id:", user)
        self.lbl_total_hours.setText("Total Hours: loading…")
        self.lbl_avg.setText("Avg / Session: loading…")
        self.lbl_sessions.setText("Sessions: loading…")
        self.table_sessions.setRowCount(0)

        w1 = ApiWorker(self.api_get_stats, user)
        w1.finished.connect(lambda data, err: self.on_stats_loaded(user, data, err))
        w1.start()
        self._w_stats = w1

    def on_stats_loaded(self, user, data, err):
        if err:
            QMessageBox.warning(self, "Stats Error", str(err))
            return

        total_sessions = data.get("total_sessions", 0)
        total_hours = float(data.get("total_hours", 0.0))
        avg_duration = float(data.get("avg_duration", 0.0))

        self.lbl_total_hours.setText(f"Total Hours: {total_hours:.2f}")
        self.lbl_avg.setText(f"Avg / Session: {avg_duration:.2f}")
        self.lbl_sessions.setText(f"Sessions: {total_sessions}")

        w2 = ApiWorker(self.api_get_sessions, user)
        w2.finished.connect(self.on_sessions_loaded)
        w2.start()
        self._w_sessions = w2

    def on_sessions_loaded(self, sessions, err):
        if err:
            QMessageBox.warning(self, "Sessions Error", str(err))
            return

        self.table_sessions.setRowCount(len(sessions))

        def pretty_hours(duration_str):
            try:
                h, m, s = duration_str.split(":")
                return float(h) + float(m) / 60.0
            except Exception:
                return 0.0

        def format_location(loc):
            if not loc:
                return "-"
            city = loc.get("city") or ""
            region = loc.get("region") or ""
            country = loc.get("country") or ""
            parts = [p for p in [city, region, country] if p]
            return ", ".join(parts) if parts else "-"

        for r, rec in enumerate(sessions):
            self.table_sessions.setItem(r, 0, QTableWidgetItem(rec.get("user_id", "")))
            self.table_sessions.setItem(r, 1, QTableWidgetItem(rec.get("session_start", "")))
            self.table_sessions.setItem(r, 2, QTableWidgetItem(rec.get("session_end", "")))

            dur = rec.get("total_duration", "0:00:00")
            self.table_sessions.setItem(
                r, 3, QTableWidgetItem(f"{pretty_hours(dur):.2f} hrs")
            )

            self.table_sessions.setItem(
                r, 4, QTableWidgetItem(format_location(rec.get("location")))
            )



    # -------- Export / Delete (same endpoints) --------
    def export_data(self):
        user = self.generate_username()
        url = f"{API_BASE_URL}/export-data"
        params = {"user_filter": user}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            records = response.json()
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", str(e))
            return

        if not records:
            QMessageBox.information(self, "Export", "No data available.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["User", "Start Time", "End Time", "Duration"])
            for rec in records:
                writer.writerow([rec["user_id"], rec["session_start"], rec["session_end"], rec["total_duration"]])

        QMessageBox.information(self, "Export Successful", "CSV exported successfully.")

    def delete_data(self):
        user = self.generate_username()

        try:
            sessions = self.api_get_sessions(user)
        except Exception as e:
            QMessageBox.warning(self, "Fetch Failed", str(e))
            return

        if not sessions:
            QMessageBox.information(self, "No Data", "No sessions to delete.")
            return

        items = [s.get("session_start", "") for s in sessions]
        item, ok = QInputDialog.getItem(self, "Delete Session", "Select a session start time:", items, 0, False)
        if not ok or not item:
            return

        confirm = QMessageBox.question(
            self, "Confirm Deletion",
            f"Delete session for:\n\n{user}\n{item}\n\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            r = requests.delete(f"{API_BASE_URL}/delete-session", json={"user": user, "session_start": item}, timeout=10)
            if r.status_code != 200:
                raise RuntimeError(r.text)
        except Exception as e:
            QMessageBox.warning(self, "Deletion Failed", str(e))
            return

        QMessageBox.information(self, "Deleted", "Session deleted.")
        self.refresh_stats()

    # -------- Activity --------
    def generate_chart_async(self):
        user = self.generate_username()
        self.btn_generate.setEnabled(False)
        self.btn_generate.setText("Generating…")

        w = ApiWorker(self.api_get_sessions, user)
        w.finished.connect(self.on_chart_data)
        w.start()
        self._w_chart = w

    def on_chart_data(self, sessions, err):
        self.btn_generate.setEnabled(True)
        self.btn_generate.setText("Generate")

        if err:
            QMessageBox.warning(self, "Chart Error", str(err))
            return
        if not sessions:
            QMessageBox.information(self, "No Data", "No activity data to display.")
            return

        def parse_duration(duration_str):
            h, m, s = duration_str.split(":")
            return float(h) + float(m) / 60.0 + float(s) / 3600.0

        timestamps = [s["session_start"] for s in sessions]
        durations = [parse_duration(s.get("total_duration", "0:00:00")) for s in sessions]

        while self.chart_layout.count():
            item = self.chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        fig, ax = plt.subplots(figsize=(12, 5))
        chart_type = self.chart_type.currentText()

        if chart_type == "Bar Chart":
            ax.bar(timestamps, durations)
            ax.set_ylabel("Hours")
        elif chart_type == "Pie Chart":
            ax.pie(durations, labels=timestamps, autopct="%1.1f%%", startangle=90)
        else:
            ax.plot(timestamps, durations, marker="o")
            ax.set_ylabel("Hours")

        ax.set_title(f"Activity for {self.generate_username()}")

        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
        canvas.draw()

    # -------- Logs --------
    def refresh_logs(self):
        user = self.generate_username()
        self.log_list.clear()
        self._logs_cache = []

        w = ApiWorker(self.api_get_logs, user)
        w.finished.connect(self.on_logs_loaded)
        w.start()
        self._w_logs = w

    def on_logs_loaded(self, logs, err):
        if err:
            QMessageBox.warning(self, "Logs Error", str(err))
            return

        self._logs_cache = logs or []
        if not self._logs_cache:
            self.log_list.addItem("No logs available.")
            return

        for log in self._logs_cache:
            self.log_list.addItem(f"ID: {log['log_id']} • {log['log_timestamp']}")

    def view_selected_log(self):
        row = self.log_list.currentRow()
        if row < 0 or row >= len(self._logs_cache):
            return

        log = self._logs_cache[row]
        details = (
            f"User: {log['user_id']}\n"
            f"Timestamp: {log['log_timestamp']}\n\n"
            f"{log['log_content']}"
        )

        dlg = QDialog(self)
        dlg.setWindowTitle("Log Details")
        dlg.setMinimumSize(760, 520)

        lay = QVBoxLayout(dlg)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setText(details)
        lay.addWidget(text)

        btn = QPushButton("Close")
        btn.clicked.connect(dlg.close)
        lay.addWidget(btn)

        dlg.exec_()

    def build_tasks_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        frame, lay = self.card(
            "Development Tasks",
            "Central tracker for eSim work: bugs, features, installers, testing, documentation "
            "with component, platform, and release linkage."
        )
        layout.addWidget(frame)

        # -------------------------
        # Filters
        # -------------------------
        filters_row = QHBoxLayout()

        self.f_task_status = QComboBox()
        self.f_task_status.addItems(["All", "Backlog", "In Progress", "Testing", "Done"])

        self.f_task_category = QComboBox()
        self.f_task_category.addItems([
            "All", "Bug", "Feature", "Enhancement",
            "Testing", "Documentation", "Installer", "Integration"
        ])

        self.f_task_platform = QComboBox()
        self.f_task_platform.addItems(["All", "Windows", "Linux", "macOS"])

        self.f_task_component = QComboBox()
        self.f_task_component.addItems([
            "All", "UI", "Ngspice", "Verilator", "GHDL", "KiCad",
            "OpenModelica", "Installer", "Docs", "Regression", "General"
        ])

        btn_apply = QPushButton("Apply Filters")
        btn_apply.setObjectName("Primary")
        btn_apply.clicked.connect(self.refresh_tasks)

        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_task_filters)

        for label, widget in [
            ("Status:", self.f_task_status),
            ("Category:", self.f_task_category),
            ("Platform:", self.f_task_platform),
            ("Component:", self.f_task_component),
        ]:
            filters_row.addWidget(QLabel(label))
            filters_row.addWidget(widget)

        filters_row.addWidget(btn_apply)
        filters_row.addWidget(btn_clear)
        lay.addLayout(filters_row)

        # -------------------------
        # Tasks Table
        # -------------------------
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(13)
        self.task_table.setHorizontalHeaderLabels([
            "Title", "Category", "Component", "Platform",
            "Status", "Priority", "Severity", "Assignee",
            "Releases", "Updated",
            "Link Release", "Edit", "Delete"
        ])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        lay.addWidget(self.task_table)

        # -------------------------
        # Buttons
        # -------------------------
        btn_row = QHBoxLayout()

        btn_add = QPushButton("Add Task")
        btn_add.setObjectName("Primary")
        btn_add.clicked.connect(self.add_task_dialog)

        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.refresh_tasks)

        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_refresh)
        btn_row.addStretch(1)
        lay.addLayout(btn_row)

        self.refresh_tasks()
        return page



    def clear_task_filters(self):
        self.f_task_status.setCurrentText("All")
        self.f_task_category.setCurrentText("All")
        self.f_task_platform.setCurrentText("All")
        self.f_task_component.setCurrentText("All")
        self.refresh_tasks()



    def link_task_to_release(self, task):
        release_id = self.choose_release_dialog()
        if not release_id:
            return

        try:
            requests.post(
                f"{API_BASE_URL}/releases/{release_id}/items",
                json={"task_id": task["task_id"]},
                timeout=10
            ).raise_for_status()

            QMessageBox.information(
                self,
                "Linked",
                f"Task '{task['title']}' linked to Release ID {release_id}"
            )
            self.refresh_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def refresh_tasks(self):
        params = {}

        if hasattr(self, "f_task_status") and self.f_task_status.currentText() != "All":
            params["status"] = self.f_task_status.currentText()
        if hasattr(self, "f_task_category") and self.f_task_category.currentText() != "All":
            params["category"] = self.f_task_category.currentText()
        if hasattr(self, "f_task_platform") and self.f_task_platform.currentText() != "All":
            params["platform"] = self.f_task_platform.currentText()
        if hasattr(self, "f_task_component") and self.f_task_component.currentText() != "All":
            params["component"] = self.f_task_component.currentText()

        try:
            r = requests.get(f"{API_BASE_URL}/tasks", params=params, timeout=10)
            r.raise_for_status()
            tasks = r.json()
        except Exception as e:
            QMessageBox.warning(self, "Tasks Error", str(e))
            return

        self.task_table.setRowCount(len(tasks))

        for i, t in enumerate(tasks):
            category = t.get("category") or t.get("task_type", "")
            labels = t.get("release_labels", [])
            releases_text = ", ".join(labels) if labels else "-"


            self.task_table.setItem(i, 0, QTableWidgetItem(t.get("title", "")))
            self.task_table.setItem(i, 1, QTableWidgetItem(category))
            self.task_table.setItem(i, 2, QTableWidgetItem(t.get("component", "General")))
            self.task_table.setItem(i, 3, QTableWidgetItem(t.get("platform", "All")))
            self.task_table.setItem(i, 4, QTableWidgetItem(t.get("status", "")))
            self.task_table.setItem(i, 5, QTableWidgetItem(t.get("priority", "")))
            self.task_table.setItem(i, 6, QTableWidgetItem(str(t.get("severity") or "")))
            self.task_table.setItem(i, 7, QTableWidgetItem(t.get("assignee", "")))

            # ✅ Releases column (from backend release_ids)
            self.task_table.setItem(i, 8, QTableWidgetItem(releases_text))

            self.task_table.setItem(i, 9, QTableWidgetItem(t.get("updated_at") or t.get("created_at", "")))

            # ✅ Link Release button
            btn_link = QPushButton("Link")
            btn_link.clicked.connect(lambda _, task=t: self.link_task_to_release(task))
            self.task_table.setCellWidget(i, 10, btn_link)

            # Edit / Delete buttons shifted right
            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, task=t: self.edit_task_dialog(task))
            self.task_table.setCellWidget(i, 11, btn_edit)

            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(lambda _, task=t: self.delete_task(task))
            self.task_table.setCellWidget(i, 12, btn_delete)


    def edit_task_dialog(self, task):
        dlg = QDialog(self)
        dlg.setWindowTitle("Edit Task")
        dlg.setMinimumWidth(520)

        form = QFormLayout(dlg)

        title = QLineEdit(task.get("title", ""))

        description = QTextEdit()
        description.setText(task.get("description", "") or "")
        description.setFixedHeight(90)

        category = QComboBox()
        category.addItems(["Bug", "Feature", "Enhancement", "Testing", "Documentation", "Installer", "Integration"])
        category.setCurrentText(task.get("category") or task.get("task_type") or "Feature")

        component = QComboBox()
        component.addItems(["UI", "Ngspice", "Verilator", "GHDL", "KiCad", "OpenModelica", "Installer", "Docs", "Regression", "General"])
        component.setCurrentText(task.get("component", "General"))

        platform = QComboBox()
        platform.addItems(["All", "Windows", "Linux", "macOS"])
        platform.setCurrentText(task.get("platform", "All"))

        status = QComboBox()
        status.addItems(["Backlog", "In Progress", "Testing", "Done"])
        status.setCurrentText(task.get("status", "Backlog"))

        priority = QComboBox()
        priority.addItems(["Low", "Medium", "High", "Critical"])
        priority.setCurrentText(task.get("priority", "Medium"))

        severity = QComboBox()
        severity.addItems(["", "Minor", "Major", "Critical"])
        severity.setCurrentText(str(task.get("severity") or ""))

        assignee = QLineEdit(task.get("assignee", "Unassigned"))

        form.addRow("Title:", title)
        form.addRow("Description:", description)
        form.addRow("Category:", category)
        form.addRow("Component:", component)
        form.addRow("Platform:", platform)
        form.addRow("Status:", status)
        form.addRow("Priority:", priority)
        form.addRow("Severity (optional):", severity)
        form.addRow("Assignee:", assignee)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form.addRow(buttons)

        def submit():
            payload = {
                "title": title.text().strip(),
                "description": description.toPlainText().strip(),
                "category": category.currentText(),
                "component": component.currentText(),
                "platform": platform.currentText(),
                "status": status.currentText(),
                "priority": priority.currentText(),
                "severity": severity.currentText() or None,
                "assignee": assignee.text().strip() or "Unassigned",
            }

            try:
                requests.put(
                    f"{API_BASE_URL}/update-task/{task['task_id']}",
                    json=payload,
                    timeout=10
                ).raise_for_status()
            except Exception as e:
                QMessageBox.critical(dlg, "Error", str(e))
                return

            dlg.accept()
            self.refresh_tasks()

        buttons.accepted.connect(submit)
        buttons.rejected.connect(dlg.reject)
        dlg.exec_()

    def delete_task(self, task):
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Are you sure you want to delete '{task['title']}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                requests.delete(
                    f"{API_BASE_URL}/delete-task/{task['task_id']}",
                    timeout=10
                ).raise_for_status()
                self.refresh_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def add_task_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Task")
        dlg.setMinimumWidth(520)

        form = QFormLayout(dlg)

        title = QLineEdit()
        title.setPlaceholderText("Short task title (e.g., Fix ngspice convergence issue)")

        description = QTextEdit()
        description.setPlaceholderText("Describe what needs to be done, steps, links, expected result…")
        description.setFixedHeight(90)

        category = QComboBox()
        category.addItems(["Bug", "Feature", "Enhancement", "Testing", "Documentation", "Installer", "Integration"])

        component = QComboBox()
        component.addItems(["UI", "Ngspice", "Verilator", "GHDL", "KiCad", "OpenModelica", "Installer", "Docs", "Regression", "General"])

        platform = QComboBox()
        platform.addItems(["All", "Windows", "Linux", "macOS"])

        status = QComboBox()
        status.addItems(["Backlog", "In Progress", "Testing", "Done"])

        priority = QComboBox()
        priority.addItems(["Low", "Medium", "High", "Critical"])

        severity = QComboBox()
        severity.addItems(["", "Minor", "Major", "Critical"])  # optional

        assignee = QLineEdit()
        assignee.setPlaceholderText("Unassigned")

        form.addRow("Title:", title)
        form.addRow("Description:", description)
        form.addRow("Category:", category)
        form.addRow("Component:", component)
        form.addRow("Platform:", platform)
        form.addRow("Status:", status)
        form.addRow("Priority:", priority)
        form.addRow("Severity (optional):", severity)
        form.addRow("Assignee:", assignee)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form.addRow(buttons)

        def submit():
            if not title.text().strip():
                QMessageBox.warning(dlg, "Validation Error", "Task title is required.")
                return

            payload = {
                "title": title.text().strip(),
                "description": description.toPlainText().strip(),
                "category": category.currentText(),
                "component": component.currentText(),
                "platform": platform.currentText(),
                "status": status.currentText(),
                "priority": priority.currentText(),
                "severity": severity.currentText() or None,
                "assignee": assignee.text().strip() or "Unassigned",
            }

            try:
                requests.post(f"{API_BASE_URL}/add-task", json=payload, timeout=10).raise_for_status()
            except Exception as e:
                QMessageBox.critical(dlg, "Error", str(e))
                return

            dlg.accept()
            self.refresh_tasks()

        buttons.accepted.connect(submit)
        buttons.rejected.connect(dlg.reject)
        dlg.exec_()

    def link_task_to_release(self, task):
        release_id = self.choose_release_dialog()
        if not release_id:
            return

        try:
            requests.post(
                f"{API_BASE_URL}/releases/{release_id}/items",
                json={"task_id": task["task_id"]},
                timeout=10
            ).raise_for_status()

            QMessageBox.information(self, "Linked", f"Task linked to Release ID {release_id}")
            self.refresh_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def choose_release_dialog(self):
        """Loads releases from backend and lets user choose one."""
        try:
            r = requests.get(f"{API_BASE_URL}/releases", timeout=10)
            r.raise_for_status()
            releases = r.json()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load releases: {e}")
            return None

        if not releases:
            QMessageBox.information(self, "Releases", "No releases found. Create one first.")
            return None

        items = [f"{rel['release_id']} • {rel['version']} • {rel['status']}" for rel in releases]
        item, ok = QInputDialog.getItem(self, "Select Release", "Choose a release:", items, 0, False)
        if not ok or not item:
            return None

        release_id = int(item.split("•")[0].strip())
        return release_id

    
    def build_releases_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        frame, lay = self.card("Releases / Milestones", "Plan versions, attach tasks, and track progress.")
        layout.addWidget(frame)

        self.release_table = QTableWidget()
        self.release_table.setColumnCount(6)
        self.release_table.setHorizontalHeaderLabels(["ID", "Version", "Status", "Target Date", "Release Date", "Notes"])
        self.release_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.release_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        lay.addWidget(self.release_table)

        btn_row = QHBoxLayout()

        btn_add = QPushButton("Add Release")
        btn_add.setObjectName("Primary")
        btn_add.clicked.connect(self.add_release_dialog)

        btn_progress = QPushButton("View Progress")
        btn_progress.clicked.connect(self.view_release_progress)

        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_progress)
        btn_row.addStretch(1)
        lay.addLayout(btn_row)

        self._releases_cache = []
        self.refresh_releases()
        return page


    def refresh_releases(self):
        try:
            self._releases_cache = requests.get(f"{API_BASE_URL}/releases", timeout=10).json()
        except Exception as e:
            QMessageBox.warning(self, "Releases Error", str(e))
            return

        self.release_table.setRowCount(len(self._releases_cache))
        for i, r in enumerate(self._releases_cache):
            self.release_table.setItem(i, 0, QTableWidgetItem(str(r["release_id"])))
            self.release_table.setItem(i, 1, QTableWidgetItem(r["version"]))
            self.release_table.setItem(i, 2, QTableWidgetItem(r["status"]))
            self.release_table.setItem(i, 3, QTableWidgetItem(str(r.get("target_date") or "")))
            self.release_table.setItem(i, 4, QTableWidgetItem(str(r.get("release_date") or "")))
            self.release_table.setItem(i, 5, QTableWidgetItem(r.get("notes","")))


    def add_release_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Add Release")
        dlg.setMinimumWidth(420)
        form = QFormLayout(dlg)

        version = QLineEdit()
        status = QComboBox()
        status.addItems(["Planned", "In Progress", "Testing", "Released"])

        target = QLineEdit()
        target.setPlaceholderText("YYYY-MM-DD (optional)")
        release_date = QLineEdit()
        release_date.setPlaceholderText("YYYY-MM-DD (optional)")
        notes = QLineEdit()

        form.addRow("Version:", version)
        form.addRow("Status:", status)
        form.addRow("Target Date:", target)
        form.addRow("Release Date:", release_date)
        form.addRow("Notes:", notes)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form.addRow(buttons)

        def submit():
            if not version.text().strip():
                QMessageBox.warning(dlg, "Validation", "Version is required.")
                return
            payload = {
                "version": version.text().strip(),
                "status": status.currentText(),
                "target_date": target.text().strip() or None,
                "release_date": release_date.text().strip() or None,
                "notes": notes.text().strip()
            }
            try:
                requests.post(f"{API_BASE_URL}/releases", json=payload, timeout=10).raise_for_status()
            except Exception as e:
                QMessageBox.critical(dlg, "Error", str(e))
                return
            dlg.accept()
            self.refresh_releases()

        buttons.accepted.connect(submit)
        buttons.rejected.connect(dlg.reject)
        dlg.exec_()


    def view_release_progress(self):
        rid = self.choose_release_dialog()
        if not rid:
            return
        try:
            data = requests.get(f"{API_BASE_URL}/releases/{rid}/progress", timeout=10).json()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            return

        by_status = data.get("by_status", {})
        msg = "\n".join([f"{k}: {v}" for k, v in by_status.items()]) or "No tasks attached."
        QMessageBox.information(self, "Release Progress", msg)

    def build_crashes_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        frame, lay = self.card(
            "Crashes",
            "Detected eSim.exe crash events (Windows Event Log). Search, filter, group & export."
        )
        layout.addWidget(frame)

        # --- Filters / Search ---
        filters = QHBoxLayout()

        self.crash_search = QLineEdit()
        self.crash_search.setPlaceholderText("Search by time / exception / module / message…")
        self.crash_search.textChanged.connect(self.apply_crash_filters)

        self.f_crash_exc = QComboBox()
        self.f_crash_exc.addItem("All")
        self.f_crash_exc.currentTextChanged.connect(self.apply_crash_filters)

        self.f_crash_mod = QComboBox()
        self.f_crash_mod.addItem("All")
        self.f_crash_mod.currentTextChanged.connect(self.apply_crash_filters)

        filters.addWidget(QLabel("Search:"))
        filters.addWidget(self.crash_search, 2)
        filters.addWidget(QLabel("Exception:"))
        filters.addWidget(self.f_crash_exc, 1)
        filters.addWidget(QLabel("Module:"))
        filters.addWidget(self.f_crash_mod, 1)

        lay.addLayout(filters)

        # --- Two-pane: list + grouped table ---
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left: crash list
        left = QVBoxLayout()
        self.crash_list = QListWidget()
        self.crash_list.currentRowChanged.connect(self._on_crash_row_changed)
        left.addWidget(self.crash_list)

        btn_row = QHBoxLayout()
        self.btn_refresh_crashes = QPushButton("Refresh")
        self.btn_refresh_crashes.setObjectName("Primary")
        self.btn_refresh_crashes.clicked.connect(self.refresh_crashes)

        self.btn_view_crash = QPushButton("View Selected Crash")
        self.btn_view_crash.setObjectName("Primary")
        self.btn_view_crash.clicked.connect(self.view_selected_crash)
        self.btn_view_crash.setEnabled(False)

        self.btn_export_crashes = QPushButton("Export Crashes CSV")
        self.btn_export_crashes.clicked.connect(self.export_crashes_csv)

        btn_row.addWidget(self.btn_refresh_crashes)
        btn_row.addWidget(self.btn_view_crash)
        btn_row.addWidget(self.btn_export_crashes)
        btn_row.addStretch(1)
        left.addLayout(btn_row)

        content.addLayout(left, 2)

        # Right: grouped signatures
        right = QVBoxLayout()
        right.addWidget(QLabel("Top Crash Signatures"))

        self.crash_group_table = QTableWidget()
        self.crash_group_table.setColumnCount(4)
        self.crash_group_table.setHorizontalHeaderLabels(["Signature", "Count", "Last Seen", "Example"])
        self.crash_group_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.crash_group_table.setEditTriggers(self.crash_group_table.NoEditTriggers)
        right.addWidget(self.crash_group_table)

        gbtn = QHBoxLayout()
        self.btn_export_groups = QPushButton("Export Summary CSV")
        self.btn_export_groups.clicked.connect(self.export_crash_groups_csv)
        gbtn.addWidget(self.btn_export_groups)
        gbtn.addStretch(1)
        right.addLayout(gbtn)

        content.addLayout(right, 3)
        lay.addLayout(content)

        # --- caches + timer ---
        self._crashes_cache = []
        self._crashes_view = []
        self._last_crash_id_seen = 0

        if not hasattr(self, "crash_timer"):
            self.crash_timer = QTimer(self)
            self.crash_timer.setInterval(30_000)  # 30s
            self.crash_timer.timeout.connect(self.poll_new_crashes)

        return page

    def refresh_crashes(self):
        user = self.generate_username()
        self.crash_list.clear()
        self._crashes_cache = []
        self._crashes_view = []
        self.btn_view_crash.setEnabled(False)

        w = ApiWorker(self.api_get_crashes, user)
        w.finished.connect(self.on_crashes_loaded)
        w.start()
        self._w_crashes = w

    def on_crashes_loaded(self, crashes, err):
        if err:
            QMessageBox.warning(self, "Crashes Error", str(err))
            return

        self._crashes_cache = crashes or []

        # Track newest id (for polling)
        try:
            self._last_crash_id_seen = max((c.get("crash_id", 0) for c in self._crashes_cache), default=0)
        except Exception:
            self._last_crash_id_seen = 0

        self.populate_crash_filter_choices()
        self.apply_crash_filters()

        # start polling only if crashes page is visible (index 3 in your stack)
        try:
            if self.stack.currentIndex() == 3:
                self.crash_timer.start()
        except Exception:
            pass


    # ---------- FILTERS ----------
    def populate_crash_filter_choices(self):
        cur_exc = self.f_crash_exc.currentText() if hasattr(self, "f_crash_exc") else "All"
        cur_mod = self.f_crash_mod.currentText() if hasattr(self, "f_crash_mod") else "All"

        excs = sorted({(c.get("exception_code") or "").strip() for c in self._crashes_cache if c.get("exception_code")})
        mods = sorted({(c.get("faulting_module") or "").strip() for c in self._crashes_cache if c.get("faulting_module")})

        self.f_crash_exc.blockSignals(True)
        self.f_crash_mod.blockSignals(True)

        self.f_crash_exc.clear()
        self.f_crash_exc.addItem("All")
        for e in excs:
            self.f_crash_exc.addItem(e)

        self.f_crash_mod.clear()
        self.f_crash_mod.addItem("All")
        for m in mods:
            self.f_crash_mod.addItem(m)

        if cur_exc in [self.f_crash_exc.itemText(i) for i in range(self.f_crash_exc.count())]:
            self.f_crash_exc.setCurrentText(cur_exc)
        if cur_mod in [self.f_crash_mod.itemText(i) for i in range(self.f_crash_mod.count())]:
            self.f_crash_mod.setCurrentText(cur_mod)

        self.f_crash_exc.blockSignals(False)
        self.f_crash_mod.blockSignals(False)


    def apply_crash_filters(self):
        text = (self.crash_search.text() or "").lower().strip()
        exc = self.f_crash_exc.currentText() if hasattr(self, "f_crash_exc") else "All"
        mod = self.f_crash_mod.currentText() if hasattr(self, "f_crash_mod") else "All"

        view = []
        for c in self._crashes_cache:
            if exc != "All" and (c.get("exception_code") or "") != exc:
                continue
            if mod != "All" and (c.get("faulting_module") or "") != mod:
                continue

            blob = " ".join([
                str(c.get("crash_time", "")),
                str(c.get("faulting_module", "")),
                str(c.get("exception_code", "")),
                str(c.get("provider", "")),
                str(c.get("message", "")),
            ]).lower()

            if text and text not in blob:
                continue

            view.append(c)

        self._crashes_view = view
        self.render_crash_list(self._crashes_view)
        self.render_crash_groups(self._crashes_view)


    def _on_crash_row_changed(self, row: int):
        self.btn_view_crash.setEnabled(0 <= row < len(self._crashes_view))


    # ---------- RENDER ----------
    def crash_signature(self, c: dict) -> str:
        exc = (c.get("exception_code") or "").strip() or "no-code"
        mod = (c.get("faulting_module") or "").strip() or "no-module"
        eid = str(c.get("event_id") or 0)
        return f"{exc} | {mod} | {eid}"


    def extract_hint(self, msg: str) -> str:
        if not msg:
            return ""
        m = re.search(r"Exception offset:\s*([0-9a-fx]+)", msg, re.IGNORECASE)
        if m:
            return f"offset {m.group(1)}"
        m = re.search(r"Faulting application path:\s*(.+)", msg, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:80]
        return ""


    def render_crash_list(self, crashes_view):
        self.crash_list.clear()
        self.btn_view_crash.setEnabled(bool(crashes_view))

        if not crashes_view:
            self.crash_list.addItem("No crashes recorded (or no matches).")
            return

        for c in crashes_view:
            reason = []
            if c.get("exception_code"):
                reason.append(c["exception_code"])
            if c.get("faulting_module"):
                reason.append(c["faulting_module"])
            reason_text = " • ".join(reason) if reason else "Unknown reason"

            hint = self.extract_hint(c.get("message", ""))

            line = f"ID: {c.get('crash_id')} • {c.get('crash_time','')} • {reason_text}"
            if hint:
                line += f" • {hint}"

            self.crash_list.addItem(line)


    def render_crash_groups(self, crashes_view):
        groups = defaultdict(list)
        for c in crashes_view:
            groups[self.crash_signature(c)].append(c)

        items = sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)
        self.crash_group_table.setRowCount(len(items))

        for r, (sig, arr) in enumerate(items):
            count = len(arr)
            last_seen = max((x.get("crash_time") or "" for x in arr), default="")
            example = (arr[0].get("message") or "").replace("\n", " ")[:80]

            self.crash_group_table.setItem(r, 0, QTableWidgetItem(sig))
            self.crash_group_table.setItem(r, 1, QTableWidgetItem(str(count)))
            self.crash_group_table.setItem(r, 2, QTableWidgetItem(last_seen))
            self.crash_group_table.setItem(r, 3, QTableWidgetItem(example))


    # ---------- DETAILS + COPY ----------
    def format_crash_report(self, c: dict) -> str:
        return (
            "=== eSim Crash Report ===\n"
            f"Crash ID: {c.get('crash_id')}\n"
            f"User: {c.get('user_id')}\n"
            f"Crash Time: {c.get('crash_time')}\n"
            f"Session Start: {c.get('session_start')}\n"
            f"Session End: {c.get('session_end')}\n"
            f"Provider: {c.get('provider')}\n"
            f"Event ID: {c.get('event_id')}\n"
            f"Exception Code: {c.get('exception_code')}\n"
            f"Faulting Module: {c.get('faulting_module')}\n"
            f"Signature: {self.crash_signature(c)}\n"
            "\n--- Message ---\n"
            f"{c.get('message','')}\n"
            f"Location: {format_location(c.get('location'))}\n"

        )


    def view_selected_crash(self):
        def format_location(loc):
            if not loc:
                return "-"
            city = loc.get("city") or ""
            region = loc.get("region") or ""
            country = loc.get("country") or ""
            parts = [p for p in [city, region, country] if p]
            return ", ".join(parts) if parts else "-"

        row = self.crash_list.currentRow()
        if row < 0 or row >= len(self._crashes_view):
            return

        c = self._crashes_view[row]

        details = (
            f"Crash ID: {c.get('crash_id')}\n"
            f"User: {c.get('user_id')}\n"
            f"Crash Time: {c.get('crash_time')}\n"
            f"Location: {format_location(c.get('location'))}\n"
            f"Session Start: {c.get('session_start')}\n"
            f"Session End: {c.get('session_end')}\n"
            f"Provider: {c.get('provider')}\n"
            f"Event ID: {c.get('event_id')}\n"
            f"Exception Code: {c.get('exception_code')}\n"
            f"Faulting Module: {c.get('faulting_module')}\n"
            f"Signature: {self.crash_signature(c)}\n"
            "\n"
            "Message:\n"
            f"{c.get('message','')}\n"
        )

        dlg = QDialog(self)
        dlg.setWindowTitle("Crash Details")
        dlg.setMinimumSize(780, 540)

        lay = QVBoxLayout(dlg)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setText(details)
        lay.addWidget(text)

        btns = QHBoxLayout()

        copy_btn = QPushButton("Copy Report")
        copy_btn.setObjectName("Primary")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.format_crash_report(c)))

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dlg.close)

        btns.addWidget(copy_btn)
        btns.addStretch(1)
        btns.addWidget(close_btn)

        lay.addLayout(btns)
        dlg.exec_()



    # ---------- AUTO POLL (since_id) ----------
    def poll_new_crashes(self):
        # Only poll if crashes page is visible (index 3 in your stack)
        try:
            if self.stack.currentIndex() != 3:
                return
        except Exception:
            return

        user = self.generate_username()
        since = self._last_crash_id_seen or None

        w = ApiWorker(lambda u: self.api_get_crashes(u, since_id=since), user)
        w.finished.connect(self.on_new_crashes_polled)
        w.start()
        self._w_crash_poll = w


    def on_new_crashes_polled(self, new_crashes, err):
        if err or not new_crashes:
            return

        # Add new crashes to cache (prepend)
        self._crashes_cache = (new_crashes or []) + self._crashes_cache

        try:
            new_max = max((c.get("crash_id", 0) for c in new_crashes), default=0)
            self._last_crash_id_seen = max(self._last_crash_id_seen, new_max)
        except Exception:
            pass

        self.populate_crash_filter_choices()
        self.apply_crash_filters()

        QMessageBox.information(self, "New Crash Detected", f"{len(new_crashes)} new crash(es) recorded.")


    # ---------- EXPORT ----------
    def export_crashes_csv(self):
        if not self._crashes_view:
            QMessageBox.information(self, "Export", "No crashes to export (current view is empty).")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Crashes CSV", "crashes.csv", "CSV Files (*.csv)")
        if not file_path:
            return

        cols = [
            "crash_id", "user_id", "crash_time",
            "location",
            "session_start", "session_end",
            "provider", "event_id", "exception_code", "faulting_module",
            "message"
        ]


        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                for c in self._crashes_view:
                    def loc_str(loc):
                        if not loc:
                            return "-"
                        parts = [loc.get("city"), loc.get("region"), loc.get("country")]
                        parts = [p for p in parts if p]
                        return ", ".join(parts) if parts else "-"

                    for c in self._crashes_view:
                        row = []
                        for k in cols:
                            if k == "location":
                                row.append(loc_str(c.get("location")))
                            else:
                                row.append(c.get(k, ""))
                        writer.writerow(row)

        except Exception as e:
            QMessageBox.warning(self, "Export Failed", str(e))
            return

        QMessageBox.information(self, "Export Successful", "Crashes exported successfully.")


    def export_crash_groups_csv(self):
        if not self._crashes_view:
            QMessageBox.information(self, "Export", "No crashes to summarize (current view is empty).")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Crash Summary CSV", "crash_summary.csv", "CSV Files (*.csv)")
        if not file_path:
            return

        groups = defaultdict(list)
        for c in self._crashes_view:
            groups[self.crash_signature(c)].append(c)

        rows = []
        for sig, arr in groups.items():
            rows.append({
                "signature": sig,
                "count": len(arr),
                "last_seen": max((x.get("crash_time") or "" for x in arr), default=""),
                "example_message": (arr[0].get("message") or "").replace("\n", " ")[:120]
            })
        rows.sort(key=lambda r: r["count"], reverse=True)

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["signature", "count", "last_seen", "example_message"])
                for r in rows:
                    writer.writerow([r["signature"], r["count"], r["last_seen"], r["example_message"]])
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", str(e))
            return

        QMessageBox.information(self, "Export Successful", "Crash summary exported successfully.")


    # ---------- API (unchanged) ----------
    def api_get_crashes(self, user_id: str, since_id: int = None):
        params = {"user": user_id}
        if since_id is not None:
            params["since_id"] = since_id
        r = requests.get(f"{API_BASE_URL}/crashes", params=params, timeout=10)
        r.raise_for_status()
        return r.json()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    QApplication.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(APP_QSS)

    window = TrackerApp()
    window.show()
    sys.exit(app.exec_())
