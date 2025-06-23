print("Starting the logging configuration...")
import logging
import re
from colorama import Fore, Style
import sys
import colorama

colorama.init()  # Initialize colorama for colored output on Windows
# Function to strip ANSI escape codes
def strip_ansi_codes(message):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', message)

# Custom filter to clean log messages for the file handler
class RemoveANSICodesFilter(logging.Filter):
    def filter(self, record):
        # Strip ANSI escape codes from the log message
        record.msg = strip_ansi_codes(record.msg)
        return True

# Custom formatter for console logs with colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Default color for all INFO logs is white
        if record.levelno == logging.INFO:
            if "success" in record.msg.lower():  # Highlight success messages in green
                log_fmt = Fore.GREEN + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL
            else:
                log_fmt = "%(asctime)s - %(levelname)s - %(message)s"  # Default INFO logs are white
        elif record.levelno == logging.WARNING:
            log_fmt = Fore.YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL
        elif record.levelno == logging.ERROR:
            log_fmt = Fore.RED + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL
        else:
            log_fmt = "%(asctime)s - %(levelname)s - %(message)s"  # Default format for other levels

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Function to configure logging
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Suppress logs from matplotlib
    logging.getLogger("matplotlib").setLevel(logging.CRITICAL)

    # File handler (ANSI codes removed)
    file_handler = logging.FileHandler("application.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(RemoveANSICodesFilter())  # Add the filter to remove ANSI codes

    # Console handler (ANSI codes retained for colored output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.flush = sys.stdout.flush  # Ensure console output is flushed immediately
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter()
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Call the logging configuration function before any other code runs
configure_logging()

# Example usage
logger = logging.getLogger(__name__)
logger.info("This is a general info message.")
logger.info("Operation completed successfully.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")


