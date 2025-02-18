from PyQt5.QtWidgets import (
    QApplication, QListWidget,QDialog,QWidget,QFileDialog, QVBoxLayout,QScrollArea,QHeaderView, QFrame,QAbstractItemView,QPushButton, QLabel, QComboBox,QMessageBox,QHBoxLayout, QFileDialog,QInputDialog,QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
import sys,platform,os
import threading
import subprocess
import csv
#from tracker import TrackerTool
import sqlite3
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton,QTextEdit
import socket
from getmac import get_mac_address

API_BASE_URL = "https://tooltracker-afxj.onrender.com"
#API_BASE_URL = "http://127.0.0.1:5000"


class TrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eSim Tool Tracker")
        self.setGeometry(100, 100, 500, 400)

        # Layout
        layout = QVBoxLayout()

        # View Statistics Button
        self.view_stats_button = QPushButton("View Statistics")
        self.view_stats_button.clicked.connect(self.view_statistics)
        layout.addWidget(self.view_stats_button)

        # View User Activity Button
        self.view_user_activity_button = QPushButton("View User Activity")
        self.view_user_activity_button.clicked.connect(self.view_user_activity)
        layout.addWidget(self.view_user_activity_button)

        # View Logs Button
        self.view_logs_button = QPushButton("View Logs")
        self.view_logs_button.clicked.connect(self.view_logs)
        layout.addWidget(self.view_logs_button)

        # Quit Button
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit_app)
        layout.addWidget(self.quit_button)


        self.setLayout(layout)
    @staticmethod
    def generate_username():
        pc_name = socket.gethostname()
        mac_address = get_mac_address()  # Get the real MAC address of the active network interface
        if mac_address:
            return f"{pc_name}_{mac_address.replace(':', '_')}"
        else:
            raise Exception("Unable to retrieve the MAC address.")

    def view_statistics(self):
        # Create the Statistics window
        stats_window = QDialog(self)
        stats_window.setWindowTitle("Statistics")
        stats_window.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout(stats_window)

        # Fetch the current user's username
        self.selected_user = self.generate_username()  # Ensure this function returns the correct username

        # Add a placeholder for the summary and table layout (Move this before calling `display_summary`)
        self.summary_container = QVBoxLayout()
        layout.addLayout(self.summary_container)

        # Display summary metrics for the specific user
        self.display_summary(stats_window, self.selected_user)

        # Export Data Button
        export_button = QPushButton("Export Data")
        export_button.clicked.connect(lambda: self.export_data(self.selected_user))
        layout.addWidget(export_button)

        # Delete Data Button
        delete_button = QPushButton("Delete Data")
        delete_button.clicked.connect(lambda: self.delete_data(self.selected_user, stats_window))
        layout.addWidget(delete_button)

        stats_window.setLayout(layout)
        stats_window.exec_()

    def export_data(self, user_filter):
        """Exports session data to a CSV file via API."""
        
        print(f"Selected User for Export: {user_filter}")  # Debugging
        
        url = f"{API_BASE_URL}/export-data"
        params = {"user_filter": user_filter}  # Correctly passing user filter
        response = requests.get(url, params=params)

        if response.status_code == 200:
            records = response.json()
            print(f"Received Records: {records}")  # Debugging

            if not records:
                QMessageBox.warning(self, "Export Failed", "No data available for export.")
                return

            # Ask user where to save the file
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "CSV Files (*.csv);;All Files (*)"
            )

            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["User", "Start Time", "End Time", "Duration"])  

                    for record in records:
                        writer.writerow([
                            record["user_id"],        
                            record["session_start"],  
                            record["session_end"],    
                            record["total_duration"]  
                        ])

                QMessageBox.information(self, "Export Successful", "Data exported successfully!")
        else:
            QMessageBox.warning(self, "Export Failed", "Failed to fetch data from server.")

    def delete_data(self, user_filter, event=None):
        """Deletes a session by calling API and allowing user selection."""
        url = f"{API_BASE_URL}/sessions"
        params = {"user": user_filter}  # Fix: Ensure correct parameter name
        response = requests.get(url, params=params)

        if response.status_code == 200:
            records = response.json()

            if not records:
                QMessageBox.warning(self, "No Data", "No sessions available to delete.")
                return

            # Create dropdown with sessions for the selected user only
            items = [f"{r['session_start']}" for r in records]  # Fix: Only show relevant sessions
            item, ok = QInputDialog.getItem(self, "Select Session", "Select a session to delete:", items, 0, False)

            if ok and item:
                session_start = item  # Only session_start is needed since user_id is fixed

                confirmation = QMessageBox.question(
                    self, "Confirm Deletion",
                    f"Are you sure you want to delete the session for '{user_filter}' at '{session_start}'?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if confirmation == QMessageBox.Yes:
                    delete_url = f"{API_BASE_URL}/delete-session"
                    delete_response = requests.delete(delete_url, json={"user": user_filter, "session_start": session_start})

                    if delete_response.status_code == 200:
                        QMessageBox.information(self, "Deletion Successful", "Session deleted successfully.")
                        self.display_summary(user_filter)  # Refresh UI after deletion
                    else:
                        QMessageBox.warning(self, "Deletion Failed", "Failed to delete session.")
        else:
            QMessageBox.warning(self, "Fetch Failed", "Failed to fetch session data.")

    def clear_layout_recursive(self, layout):
        # Loop through all items in the layout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()  # Remove the widget
            elif item.layout():
                self.clear_layout_recursive(item.layout())  # Recursively clear nested layouts

    def display_summary(self, stats_window, user_filter=None):
        # Ensure `user_filter` is always set to the logged-in user
        current_user = self.generate_username()  # Get the generated username
        user_filter = current_user  # Override the user filter

        # Clear existing data in the summary layout
        self.clear_layout_recursive(self.summary_container)
        summary_layout = QVBoxLayout()

        try:
            # Make API request to get statistics for the current user only
            api_url = f"{API_BASE_URL}/statstics"
            params = {"user": user_filter}

            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error if the request fails
            data = response.json()

            # Extract statistics
            total_sessions = data.get("total_sessions", 0)
            total_hours = data.get("total_hours", 0.0)
            avg_duration = data.get("avg_duration", 0.0)

            # Display summary metrics
            metrics = [
                ("Total Hours Logged:", f"{total_hours:.2f} hours"),
                ("Average Duration per Session:", f"{avg_duration:.2f} hours"),
                ("Total Number of Sessions:", total_sessions),
            ]

            for label_text, value_text in metrics:
                metric_layout = QHBoxLayout()
                label = QLabel(f"<b>{label_text}</b>")
                value = QLabel(str(value_text))
                metric_layout.addWidget(label)
                metric_layout.addWidget(value)
                summary_layout.addLayout(metric_layout)

            self.summary_container.addLayout(summary_layout)

            # Fetch session details from API for the current user
            api_url_sessions = f"{API_BASE_URL}/sessions"
            response_sessions = requests.get(api_url_sessions, params=params)
            response_sessions.raise_for_status()
            sessions = response_sessions.json()

            # Create table for individual session details
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["User", "Start Time", "End Time", "Duration"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)

            # Populate table with session data
            table.setRowCount(len(sessions))
            for row_index, records in enumerate(sessions):
                table.setItem(row_index, 0, QTableWidgetItem(records["user_id"]))
                table.setItem(row_index, 1, QTableWidgetItem(records["session_start"]))
                table.setItem(row_index, 2, QTableWidgetItem(records["session_end"]))
                table.setItem(row_index, 3, QTableWidgetItem(f"{float(records['total_duration'].split(':')[0]) + float(records['total_duration'].split(':')[1]) / 60:.2f} hrs"))

            self.summary_container.addWidget(table)

        except requests.RequestException as e:
            print(f"API Request Error: {e}")

    def view_user_activity(self):
        """Fetch and display activity data for the logged-in user."""
        activity_window = QDialog(self)
        activity_window.setWindowTitle("User Activity")
        activity_window.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout(activity_window)

        # Dropdown for selecting chart type
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Bar Chart", "Pie Chart", "Line Chart"])
        self.chart_type.setCurrentText("Bar Chart")
        layout.addWidget(self.chart_type)

        # Button to generate chart
        generate_btn = QPushButton("Generate Chart")
        generate_btn.clicked.connect(lambda: self.generate_chart(activity_window))
        layout.addWidget(generate_btn)

        # Scrollable area for the chart
        self.scroll_area = QScrollArea(activity_window)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Chart container
        self.chart_container = QWidget()
        self.scroll_area.setWidget(self.chart_container)
        self.chart_layout = QVBoxLayout(self.chart_container)

        activity_window.setLayout(layout)
        activity_window.exec_()

    def generate_chart(self, activity_window):
        """Fetch session data for the logged-in user and generate a chart."""
        current_user = self.generate_username()  # Get the logged-in user
        response = requests.get(f"{API_BASE_URL}/sessions", params={"user": current_user})

        if response.status_code != 200 or not response.json():
            QMessageBox.information(activity_window, "No Data", "No activity data to display.")
            return
        def parse_duration(duration_str):
            """Convert 'HH:MM:SS.ssssss' to total hours as a float."""
            h, m, s = map(float, duration_str.split(":"))  # Convert each part to float
            return h + (m / 60) + (s / 3600)  # Convert to total hours
        # Extract session data
        sessions = response.json()
        timestamps = [s['session_start'] for s in sessions]
        durations = [parse_duration(s['total_duration']) for s in sessions]  # Convert durations correctly

        # Clear previous chart
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(15, 6))
        chart_type = self.chart_type.currentText()

        # Generate the selected chart type
        if chart_type == "Bar Chart":
            ax.bar(timestamps, durations, color='skyblue')
            ax.set_title(f'Activity Log for {current_user} (Bar Chart)', fontsize=14)
            ax.set_xlabel('Session Start Time', fontsize=12)
            ax.set_ylabel('Duration (hours)', fontsize=12)
        elif chart_type == "Pie Chart":
            ax.pie(durations, labels=timestamps, autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Activity Log for {current_user} (Pie Chart)', fontsize=14)
        elif chart_type == "Line Chart":
            ax.plot(timestamps, durations, marker='o', color='blue')
            ax.set_title(f'Activity Log for {current_user} (Line Chart)', fontsize=14)
            ax.set_xlabel('Session Start Time', fontsize=12)
            ax.set_ylabel('Duration (hours)', fontsize=12)

        # Embed Matplotlib figure into PyQt5
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
        canvas.draw()

    def view_logs(self):
        """Fetch and display logs only for the logged-in user."""
        # Create the logs window
        logs_window = QDialog(self)
        logs_window.setWindowTitle("View Logs")
        logs_window.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(logs_window)

        # Get the logged-in user's username
        current_user = self.generate_username()

        # Fetch logs from the API for the current user
        url = f"{API_BASE_URL}/logs"
        params = {"user": current_user}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            logs = response.json()
        else:
            logs = []

        if not logs:
            no_logs_label = QLabel("No logs available for this user.", logs_window)
            no_logs_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(no_logs_label)
            logs_window.setLayout(layout)
            logs_window.exec_()
            return

        # List widget for displaying logs
        log_list_widget = QListWidget(logs_window)
        for log in logs:
            log_list_widget.addItem(f"ID: {log['log_id']}, Timestamp: {log['log_timestamp']}")

        layout.addWidget(log_list_widget)

        #Function to show selected log details
        def show_selected_log():
           
            selected_item = log_list_widget.currentItem()
            if selected_item:
                selected_index = log_list_widget.row(selected_item)
                log = logs[selected_index]
                log_details = f"User: {log['user_id']}\nTimestamp: {log['log_timestamp']}\n\nLog Content:\n{log['log_content']}"

                # Create a QDialog instead of QMessageBox
                log_dialog = QDialog(logs_window)
                log_dialog.setWindowTitle("Log Details")
                log_dialog.setGeometry(200, 200, 700, 500)  # Set initial size
                log_dialog.setSizeGripEnabled(True)  # Enable window resizing

                # Create a QVBoxLayout
                layout = QVBoxLayout(log_dialog)

                # Create a QTextEdit (scrollable) to display the log content
                log_text_edit = QTextEdit(log_dialog)
                log_text_edit.setText(log_details)
                log_text_edit.setReadOnly(True)  # Make it read-only
                log_text_edit.setMinimumSize(600, 400)  # Ensure a good default size

                # Add the text edit widget to the layout
                layout.addWidget(log_text_edit)

                # Close button
                close_button = QPushButton("Close", log_dialog)
                close_button.clicked.connect(log_dialog.close)
                layout.addWidget(close_button)

                log_dialog.setLayout(layout)
                log_dialog.exec_()

        
        # View button to show the selected log's details
        view_btn = QPushButton("View Selected Log", logs_window)
        view_btn.clicked.connect(show_selected_log)

        layout.addWidget(view_btn)

        logs_window.setLayout(layout)
        logs_window.exec_()


    def quit_app(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrackerApp()
    window.show()
    sys.exit(app.exec_())