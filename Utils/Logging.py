import logging
import re
from colorama import Fore, Style

# Function to strip ANSI escape codes
def strip_ansi_codes(message):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', message)

# Custom filter to clean log messages
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
console_formatter = logging.Formatter(
    Fore.GREEN + "%(asctime)s - %(levelname)s - %(message)s" + Style.RESET_ALL
)
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example log messages
logger.info(Fore.GREEN + "This is a success message." + Style.RESET_ALL)
logger.error(Fore.RED + "This is an error message." + Style.RESET_ALL)
