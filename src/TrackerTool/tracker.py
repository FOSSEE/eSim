import psutil
import time
from datetime import datetime
import os,glob
import requests
import socket

# def generate_username():
#     pc_name = socket.gethostname()
#     mac_address = '_'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(40, -1, -8))
#     return f"{pc_name}_{mac_address}"
from getmac import get_mac_address

def generate_username():
    pc_name = socket.gethostname()
    mac_address = get_mac_address()  # Get the real MAC address of the active network interface
    if mac_address:
        return f"{pc_name}_{mac_address.replace(':', '_')}"
    else:
        raise Exception("Unable to retrieve the MAC address.")
# API base URL for the Flask app hosted locally or on Render
API_BASE_URL = "https://tooltracker-afxj.onrender.com/"
LOG_DIR = os.path.join(os.getcwd(), "logs")  # Dynamically set the log directory

# Function to send session data to the Flask API
def send_session_to_api(user_id, session_start, session_end, total_duration):
    data = {
        "user_id": user_id,
        "session_start": session_start.strftime('%Y-%m-%d %H:%M:%S'),
        "session_end": session_end.strftime('%Y-%m-%d %H:%M:%S'),
        "total_duration": f"{total_duration} hours"
    }
    try:
        response = requests.post(f"{API_BASE_URL}/add-session", json=data)
        print(f"Session API Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending session data to API: {e}")

# Function to send log data to the Flask API
def send_log_to_api(user_id, log_timestamp, log_content):
    data = {
        "user_id": user_id,
        "log_timestamp": log_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "log_content": log_content
    }
    try:
        response = requests.post(f"{API_BASE_URL}/add-log", json=data)
        print(f"Log API Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log data to API: {e}")

# Ensure log directory exists
def ensure_log_directory():
    if not os.path.exists(LOG_DIR):
        print(f"Creating log directory: {LOG_DIR}")
        os.makedirs(LOG_DIR)

# Function to log session details and send them to the API
def log_session(user_id, session_start, session_end):
    total_duration = (session_end - session_start).total_seconds() / 3600  # Duration in hours
    send_session_to_api(user_id, session_start, session_end, total_duration)

# Function to store logs and send them to the API
# def store_log(user_id):
#     log_file_path = os.path.join(LOG_DIR, f"{user_id}_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
#     try:
#         # Write some dummy content to simulate eSim logs
#         with open(log_file_path, 'w') as file:
#             file.write(f"Log initialized for user {user_id} at {datetime.now()}\n")

#         # Read and send the log content
#         with open(log_file_path, 'r') as file:
#             log_content = file.read()
#         send_log_to_api(user_id, datetime.now(), log_content)
#     except Exception as e:
#         print(f"Error handling log file: {e}")
# LOG_DIR = "/home/mmn/Downloads/eSim-2.4/src/frontEnd/logs"
LOG_DIR = os.path.join(os.getcwd(), "logs")

def store_log(user_id):
    """Finds the latest log file for the user and sends it to the API."""
    try:
        # Find the latest log file for the user
        log_files = sorted(
            glob.glob(os.path.join(LOG_DIR, f"{user_id}_log_*.txt")),
            key=os.path.getmtime,  # Sort by modification time (latest last)
            reverse=True  # Get latest file first
        )

        if not log_files:
            print(f"No log file found for user {user_id}.")
            return

        latest_log_file = log_files[0]  # Get the most recent log file

        # Read and send the log content
        with open(latest_log_file, 'r') as file:
            log_content = file.read()

        send_log_to_api(user_id, datetime.now(), log_content)

    except Exception as e:
        print(f"Error handling log file: {e}")
# Check if eSim is running
def is_esim_running():
    for process in psutil.process_iter(['name']):
        if 'esim' in process.info['name'].lower():
            return True
    return False

# Track user activity
def track_activity(user_id):
    session_start = None
    ensure_log_directory()

    print(f"Tracking started for user: {user_id}")
    try:
        while True:
            if is_esim_running():
                if session_start is None:
                    session_start = datetime.now()
                    print(f"Session started at {session_start}")
            else:
                if session_start:
                    session_end = datetime.now()
                    log_session(user_id, session_start, session_end)
                    store_log(user_id)
                    print(f"Session ended at {session_end}")
                    print(f"Duration: {(session_end - session_start)}")
                    session_start = None
            time.sleep(1)  # Check every 2 seconds
    except KeyboardInterrupt:
        print("Tracking stopped.")

# Main entry point
if __name__ == "__main__":
    user_id = generate_username()
    # consent = input("Do you consent to activity tracking? (yes/no): ")
    # if consent.lower() == 'yes':
    track_activity(user_id)
    # else:
    print("Tracking aborted. Consent not given.")
