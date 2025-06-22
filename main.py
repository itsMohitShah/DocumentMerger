import os
from PyPDF2 import PdfReader, PdfWriter
import spacy
import datetime
import re
import webbrowser
from Utils.LinkedInSearcher import extract_name_from_pdf, search_linkedin, main_linkedin_search
from Utils.MiscUtils import find_most_recent_pdf
from Utils.DocumentMerger import merge_pdfs, main_merger
from Utils.ChartMaker import read_pdfs_and_prepare_chart, prepare_chart_data, generate_chart, main_chart




if __name__ == "__main__":
    # Main logic
    path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"

    main_merger(path_CoverLetters, path_LOR)
    main_chart(path_CoverLetters)
    main_linkedin_search(path_CoverLetters)
