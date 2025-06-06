import os
from PyPDF2 import PdfReader, PdfWriter

path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters"

# Find the most recent PDF in the Cover Letters directory
def find_most_recent_pdf(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the directory.")
    
    pdf_files_with_paths = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in pdf_files]
    most_recent_pdf = max(pdf_files_with_paths, key=lambda x: x[1])[0]
    return most_recent_pdf

# Merge PDFs
def merge_pdfs(pdf1_path, pdf2_path, output_path):
    pdf_writer = PdfWriter()

    # Read and append the first PDF
    pdf1_reader = PdfReader(pdf1_path)
    for page in pdf1_reader.pages:
        pdf_writer.add_page(page)

    # Read and append the second PDF
    pdf2_reader = PdfReader(pdf2_path)
    for page in pdf2_reader.pages:
        pdf_writer.add_page(page)

    # Write the merged PDF to the output file
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

# Main logic
try:
    most_recent_pdf = find_most_recent_pdf(path_CoverLetters)
    original_pdf_name = os.path.splitext(os.path.basename(most_recent_pdf))[0]
    
    # Replace "Cover Letter" with "Cover Letter with LOR"
    if "Cover Letter" in original_pdf_name:
        output_file_name = original_pdf_name.replace("Cover Letter", "Cover Letter with LOR") + ".pdf"
    else:
        output_file_name = original_pdf_name + " - with LOR.pdf"
    
    output_path = os.path.join(path_CoverLetters, output_file_name)
    merge_pdfs(most_recent_pdf, path_LOR, output_path)
    print(f"Merged PDF saved to: {output_path}")
except Exception as e:
    print(f"An error occurred: {e}")