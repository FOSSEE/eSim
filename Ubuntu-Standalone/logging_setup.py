# logging_setup.py
import logging

# Configure logging
logging.basicConfig(
    filename="tool_manager.log",
    filemode="a",  # Append mode
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Set to DEBUG for detailed logs
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)