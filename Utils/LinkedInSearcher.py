import re
import webbrowser
from PyPDF2 import PdfReader
import os
import spacy
from Utils.MiscUtils import find_most_recent_pdf
def extract_companyname(pdf_path):
    name_pdf = os.path.basename(pdf_path)
    company_name = name_pdf.split("-")[-1]
    company_name = company_name.replace(".pdf", "").strip()
    return company_name


def extract_name_from_pdf(pdf_path):
    """
    Reads a PDF file and extracts the name from the letter.
    Assumes the name appears after a keyword like 'Dear'.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted name, or None if no name is found.
    """
    try:
        # Read the PDF
        reader = PdfReader(pdf_path)
        text = ""
        
        # Extract text from all pages
        for page in reader.pages:
            text += page.extract_text()
        nlp = spacy.load("en_core_web_trf")  # Load the spaCy model
        doc = nlp(text)
        name = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                ent_text = ent.text.strip()
                if ent_text.lower() == "mohit shah" or ent_text.lower() == "jan erxleben" or ent_text.lower() == "nirav doshi":
                    continue
                name.append(ent.text)
        name = list(set(name))  # Remove duplicates
        return name if name else None                
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def search_linkedin(list_names, companyname):
    """
    Performs a LinkedIn search for the given name.

    Args:
        name (str): The name to search for on LinkedIn.

    Returns:
        None
    """
    if not list_names:
        print("No name provided for LinkedIn search.")
        return

    # Construct the LinkedIn search URL
    base_url = "https://www.linkedin.com/search/results/people/?keywords="
    for name in (list_names):
        name = name.strip()  # Clean up the name
        if not name:
            continue
        # Construct the search URL for each name    
        search_query = f"{name} {companyname}"
        search_url = base_url + search_query.replace(" ", "%20")  # Replace spaces with URL-encoded '%20'

        # Open the search URL in the default web browser
        webbrowser.open(search_url, new = 1)
        print(f"Searching LinkedIn for: {name}")


def main_linkedin_search(pdf_path):
    """
    Extracts the name from a PDF and performs a LinkedIn search.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        None
    """
    most_recent_pdf = find_most_recent_pdf(pdf_path)
    companyname = extract_companyname(most_recent_pdf)
    name = extract_name_from_pdf(most_recent_pdf)
    if name:
        search_linkedin(name, companyname)
    else:
        print("No valid name found in the PDF for LinkedIn search.")