import sys
import os
import time
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt

DOWNLOAD_DIR = r"C:\FOSSEE\Tool-Manager\Download"

ghdl_packages = {
    "https://github.com/ghdl/ghdl/releases/download/v4.1.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst": "ghdl-v4.1.0.pkg.tar.zst"
}

kicad_installers = {
    "https://downloads.kicad.org/kicad/windows/explore/stable/download/kicad-8.0.9-x86_64.exe": "kicad-8.0.9.exe"
}

verilator_packages = {
    "https://github.com/verilator/verilator/releases/download/v5.016/verilator-5.016-win64.zip": "verilator.zip"
}
ngspice_packages = {
    "https://sourceforge.net/projects/ngspice/files/ng-spice-rework/42/ngspice-42_64.zip/download": "ngspice-42.zip"
}
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_RETRIES = 3


class DownloadWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tool Manager")
        self.setGeometry(500, 200, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Ready to Download")
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

        self.button = QPushButton("Start Download")
        self.button.clicked.connect(self.start_download)

        self.redownload_button = QPushButton("Re-download")
        self.redownload_button.clicked.connect(self.force_download)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.button)
        layout.addWidget(self.redownload_button)

        self.setLayout(layout)

    def update_progress(self, value):
        self.progress.setValue(value)
        QApplication.processEvents()

    def download_file(self, url, save_path, progress_callback):
        for attempt in range(MAX_RETRIES):
            try:
                with requests.get(url, headers=HEADERS, stream=True) as r:
                    total_size = int(r.headers.get('content-length', 0))
                    downloaded = 0

                    with open(save_path, "wb") as f:
                        for chunk in r.iter_content(1024 * 1024):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)

                                if total_size > 0:
                                    percent = int((downloaded / total_size) * 100)
                                    progress_callback(percent)

                                QApplication.processEvents()

                return True

            except Exception as e:
                print("Retry...", e)
                time.sleep(2)

        return False

    def start_download(self):
        self.button.setEnabled(False)
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        all_files = []
        all_files += list(ghdl_packages.items())
        all_files += list(kicad_installers.items())
        all_files += list(verilator_packages.items())
        all_files += list(ngspice_packages.items())

    # ✅ CHECK: Are all files already downloaded?
        already_downloaded = True
        for url, filename in all_files:
            save_path = os.path.join(DOWNLOAD_DIR, filename)
            if not os.path.exists(save_path):
                already_downloaded = False
                break

        if already_downloaded:
            QMessageBox.information(self, "Info", "All tools are already downloaded! Nothing to do.")
            self.button.setEnabled(True)
            return

    # ✅ Continue download if not all present
        total_files = len(all_files)
        current_file = 0

        for url, filename in all_files:
            save_path = os.path.join(DOWNLOAD_DIR, filename)

        # Skip already downloaded files
            if os.path.exists(save_path):
                current_file += 1
                continue

            def file_progress(p):
                overall = int((current_file / total_files) * 100 + (p / total_files))
                self.update_progress(overall)

            self.label.setText(f"Downloading: {filename}")
            self.download_file(url, save_path, file_progress)

            current_file += 1

        self.progress.setValue(100)
        self.label.setText("Download Complete")
        QMessageBox.information(self, "Done", "All tools downloaded successfully!")
        self.button.setEnabled(True)
        self.progress.setValue(0)


    def force_download(self):
        reply = QMessageBox.question(
            self,
            "Confirm Re-download",
            "This will re-download all files. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        self.button.setEnabled(False)
        self.redownload_button.setEnabled(False)

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        all_files = []
        all_files += list(ghdl_packages.items())
        all_files += list(kicad_installers.items())
        all_files += list(verilator_packages.items())
        all_files += list(ngspice_packages.items())

        total_files = len(all_files)
        current_file = 0

        for url, filename in all_files:
            save_path = os.path.join(DOWNLOAD_DIR, filename)

            def file_progress(p):
                overall = int((current_file / total_files) * 100 + (p / total_files))
                self.update_progress(overall)

            self.label.setText(f"Re-downloading: {filename}")
            self.download_file(url, save_path, file_progress)

            current_file += 1

        self.progress.setValue(100)
        self.label.setText("Re-download Complete")
        QMessageBox.information(self, "Done", "All tools re-downloaded successfully!")

        self.button.setEnabled(True)
        self.redownload_button.setEnabled(True)
        self.progress.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadWindow()
    window.show()
    sys.exit(app.exec_())