import os
import datetime
from Utils.Logging import logger  # Import the logger from your Logging module


# Find the most recent PDF in the Cover Letters directory
def find_most_recent_pdf(directory):
    try:
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the directory.")
        
        pdf_files_with_paths = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in pdf_files]
        most_recent_pdf = max(pdf_files_with_paths, key=lambda x: x[1])[0]
        logger.info(f"Most recent PDF found: {most_recent_pdf}")
        return most_recent_pdf
    except Exception as e:
        logger.error(f"Error finding the most recent PDF: {e}")
        raise

