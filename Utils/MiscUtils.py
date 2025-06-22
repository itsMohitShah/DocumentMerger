import os
import datetime
# Find the most recent PDF in the Cover Letters directory
def find_most_recent_pdf(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the directory.")
    
    pdf_files_with_paths = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in pdf_files]
    most_recent_pdf = max(pdf_files_with_paths, key=lambda x: x[1])[0]
    return most_recent_pdf

