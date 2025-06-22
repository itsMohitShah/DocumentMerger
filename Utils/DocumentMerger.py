print( "Loading DocumentMerger module ...")
from PyPDF2 import PdfReader, PdfWriter
import os
import logging
from colorama import Fore, Style
from Utils.MiscUtils import find_most_recent_pdf

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Merge PDFs
def merge_pdfs(pdf1_path, pdf2_path, output_path):
    try:
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

        logging.info(Fore.GREEN + f"PDFs merged successfully and saved to: {output_path}" + Style.RESET_ALL)
    except Exception as e:
        logging.error(Fore.RED + f"Error merging PDFs: {e}" + Style.RESET_ALL)
        raise


def main_merger(path_CoverLetters, path_LOR):
    try:
        most_recent_pdf = find_most_recent_pdf(path_CoverLetters)
        original_pdf_name = os.path.splitext(os.path.basename(most_recent_pdf))[0]

        # Replace "Cover Letter" with "Cover Letter with LOR"
        if "Cover Letter" in original_pdf_name:
            output_file_name = original_pdf_name.replace("Cover Letter", "Cover Letter with LOR") + ".pdf"
        else:
            output_file_name = original_pdf_name + " - with LOR.pdf"

        # Save the output file in one folder above the Cover Letters path
        parent_folder = os.path.dirname(path_CoverLetters)
        output_path = os.path.join(parent_folder, output_file_name)
        merge_pdfs(most_recent_pdf, path_LOR, output_path)
    except Exception as e:
        logging.error(Fore.RED + f"Error in main merger process: {e}" + Style.RESET_ALL)