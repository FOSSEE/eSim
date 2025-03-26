import os
import time
import requests
from PyQt5.QtWidgets import QApplication, QMessageBox

# Define the download directory
DOWNLOAD_DIR = r"C:\FOSSEE\Tool-Manager\Download"

# URLs and their respective renamed filenames
ghdl_packages = {
    "https://github.com/ghdl/ghdl/releases/download/v4.1.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst": "ghdl-v4.1.0.pkg.tar.zst",
    "https://github.com/ghdl/ghdl/releases/download/v4.0.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst": "ghdl-v4.0.0.pkg.tar.zst",
    "https://github.com/ghdl/ghdl/releases/download/v3.0.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst": "ghdl-v3.0.0.pkg.tar.zst"
}

kicad_installers = {
    "https://downloads.kicad.org/kicad/windows/explore/stable/download/kicad-7.0.11-rc3-x86_64.exe": "kicad-7.0.11.exe",
    "https://downloads.kicad.org/kicad/windows/explore/stable/download/kicad-8.0.9-x86_64.exe": "kicad-8.0.9.exe"
}

# User-Agent header (to bypass 403 error)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Retry settings
MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

def download_pkg_file(url, save_path):
    """Simple direct download for .pkg.tar.zst files."""
    if os.path.exists(save_path):
        print(f"File already exists: {save_path}, skipping download.")
        return

    print(f"Downloading {url}...")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded successfully: {save_path}")
            return
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Download failed: {url}")

def download_exe_file(url, save_path):
    """Resumable download for large .exe files (KiCad installers) with retry support."""
    temp_path = save_path + ".part"  # Temporary file for incomplete downloads
    resume_header = {}

    if os.path.exists(temp_path):
        downloaded_size = os.path.getsize(temp_path)
        resume_header["Range"] = f"bytes={downloaded_size}-"
        print(f"Resuming download for {save_path} from byte {downloaded_size}...")
    else:
        print(f"Starting download for {save_path}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with requests.get(url, headers={**HEADERS, **resume_header}, stream=True) as response:
                response.raise_for_status()

                with open(temp_path, "ab") as file:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):  # Download in 1MB chunks
                        if chunk:
                            file.write(chunk)

            os.rename(temp_path, save_path)  # Rename to final file
            print(f"Downloaded successfully: {save_path}")
            return

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Download failed: {url}")

def download_packages():
    """Download both GHDL packages and KiCad installers."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Download GHDL packages (.pkg.tar.zst) using direct method
    for url, filename in ghdl_packages.items():
        save_path = os.path.join(DOWNLOAD_DIR, filename)
        download_pkg_file(url, save_path)

    # Download KiCad installers (.exe) using resumable method
    for url, filename in kicad_installers.items():
        save_path = os.path.join(DOWNLOAD_DIR, filename)
        download_exe_file(url, save_path)

    show_popup_message()

def show_popup_message():
    """Show a pop-up message after all downloads are complete."""
    app = QApplication([])  # Create a QApplication instance
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("All packages have been downloaded successfully.")
    msg.setWindowTitle("Download Complete")
    msg.exec_()

if __name__ == "__main__":
    download_packages()
