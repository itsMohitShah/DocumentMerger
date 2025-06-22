import os
import datetime
import logging
from colorama import Fore, Style

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Find the most recent PDF in the Cover Letters directory
def find_most_recent_pdf(directory):
    try:
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the directory.")
        
        pdf_files_with_paths = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in pdf_files]
        most_recent_pdf = max(pdf_files_with_paths, key=lambda x: x[1])[0]
        logging.info(Fore.GREEN + f"Most recent PDF found: {most_recent_pdf}" + Style.RESET_ALL)
        return most_recent_pdf
    except Exception as e:
        logging.error(Fore.RED + f"Error finding the most recent PDF: {e}" + Style.RESET_ALL)
        raise

