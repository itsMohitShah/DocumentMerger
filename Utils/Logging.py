import logging
import re
from colorama import Fore, Style

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

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
# File handler (ANSI codes removed)
file_handler = logging.FileHandler("application.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
file_handler.addFilter(RemoveANSICodesFilter())  # Add the filter to remove ANSI codes

# Console handler (ANSI codes retained for colored output)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Custom formatter for console logs with colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.msg = Fore.GREEN + record.msg + Style.RESET_ALL
        elif record.levelno == logging.WARNING:
            record.msg = Fore.YELLOW + record.msg + Style.RESET_ALL
        elif record.levelno == logging.ERROR:
            record.msg = Fore.RED + record.msg + Style.RESET_ALL
        return super().format(record)

console_formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example log messages
logger.info("This is a success message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
