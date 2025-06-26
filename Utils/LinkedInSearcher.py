print("Loading LinkedInSearcher module ...")
import time
import re
import webbrowser
from PyPDF2 import PdfReader
import os
import logging
from Utils.Logging import logger  # Import the logger from your Logging module
from colorama import Fore, Style
from Utils.MiscUtils import find_most_recent_pdf
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def extract_companyname(pdf_path):
    """
    Extracts the company name from the PDF file name.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted company name, or None if an error occurs.
    """
    try:
        logger.info(f"Extracting company name from PDF: {pdf_path}")
        name_pdf = os.path.basename(pdf_path)
        company_name = name_pdf.split("-")[-1]
        company_name = company_name.replace(".pdf", "").strip()
        logger.info(Fore.GREEN + f"Extracted company name: {company_name}" + Style.RESET_ALL)
        return company_name
    except Exception as e:
        logger.error(Fore.RED + f"Error extracting company name: {e}" + Style.RESET_ALL)
        return None


def filter_full_names(name_list):
    """
    Filters a list of names to keep only the full names if both a last name and a full name are present.

    Args:
        name_list (list): A list of names (e.g., ["Doe", "John Doe"]).

    Returns:
        list: A filtered list containing only the full names.
    """
    try:
        logger.info(f"Filtering full names from the list: {name_list}")
        full_names_only = []
        for current_name in name_list:
            # Check if the current name is a substring of any other name in the list
            is_substring = any(
                current_name != other_name and current_name in other_name
                for other_name in name_list
            )
            if not is_substring:
                full_names_only.append(current_name)
        logger.info(f"Filtered full names: {full_names_only}")
        return full_names_only
    except Exception as e:
        logger.error(Fore.RED + f"Error filtering full names: {e}" + Style.RESET_ALL)
        return []


def extract_name_from_pdf(pdf_path):
    """
    Reads a PDF file and extracts the name from the letter.
    Assumes the name appears after a keyword like 'Dear'.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: Extracted names, or None if no names are found.
    """
    try:
        logger.info(f"Extracting names from PDF: {pdf_path}")
        # Read the PDF
        reader = PdfReader(pdf_path)
        text = ""
        
        # Extract text from all pages
        for page in reader.pages:
            text += page.extract_text()
        logger.info("Extracted PDF text")
        import spacy

        # Use spaCy to extract names
        logger.info("Loading spaCy model for name extraction...")

        nlp = spacy.load("en_core_web_trf")

        logger.info(Fore.GREEN + f"spaCy model loaded" + Style.RESET_ALL)
        doc = nlp(text)
        list_names = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                ent_text = ent.text.strip()
                if ent_text.lower() in ["mohit shah", "jan erxleben", "nirav doshi"]:
                    logger.info(f"Skipping excluded name: {ent_text}")
                    continue
                list_names.append(ent.text)
        logger.info(f"Extracted raw names: {list_names}")
        # Remove duplicates
        list_names = list(set(list_names))
        # Filter full names
        list_names = filter_full_names(list_names)
        # swape the first and last names if they are in the format "Last, First"
        list_names = [re.sub(r'(\w+) (\w+)', r'\2 \1', name) for name in list_names]
        logger.info(Fore.GREEN + f"Final extracted names: {list_names}" + Style.RESET_ALL)
        return list_names if list_names else None
    except Exception as e:
        logger.error(Fore.RED + f"Error extracting name from PDF: {e}" + Style.RESET_ALL)
        return None


def search_linkedin(list_names, companyname):
    """
    Performs a LinkedIn search for the given names and company.

    Args:
        list_names (list): List of names to search for on LinkedIn.
        companyname (str): The company name to include in the search.

    Returns:
        None
    """
    try:
        if not list_names:
            logger.warning(Fore.YELLOW + "No names provided for LinkedIn search." + Style.RESET_ALL)
            return
        logger.info(f"Starting LinkedIn search for names: {list_names} and company: {companyname}")
        # Construct the LinkedIn search URL
        base_url = "https://www.linkedin.com/search/results/people/?keywords="
        for name in list_names:
            name = name.strip()  # Clean up the name
            if not name:
                continue
            # Construct the search URL for each name    
            search_query = f"{name} {companyname}"
            search_url = base_url + search_query.replace(" ", "%20")  # Replace spaces with URL-encoded '%20'

            # Open the search URL in the default web browser
            logger.info(Fore.GREEN + f"Searching LinkedIn for: {search_query}" + Style.RESET_ALL)
            webbrowser.open(search_url, new=1)
            if len(list_names) > 1:
                wait_time = 2  # Wait time in seconds
                logger.info(Fore.BLUE + f"Waiting for {wait_time} seconds before opening the next search." + Style.RESET_ALL)
                time.sleep(wait_time)  # Wait before opening the next search
        logger.info(Fore.GREEN + "LinkedIn search completed." + Style.RESET_ALL)
    except Exception as e:
        logger.error(Fore.RED + f"Error during LinkedIn search: {e}" + Style.RESET_ALL)


def main_linkedin_search(pdf_path):
    """
    Extracts the name from a PDF and performs a LinkedIn search.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: List of extracted names, or None if no names are found.
    """
    try:
        logger.info(f"Starting LinkedIn search process for PDF: {pdf_path}")
        most_recent_pdf = find_most_recent_pdf(pdf_path)
        logger.info(f"Most recent PDF found: {most_recent_pdf}")

        companyname = extract_companyname(most_recent_pdf)
        list_names = extract_name_from_pdf(most_recent_pdf)
        if list_names:
            search_linkedin(list_names, companyname)
            return list_names
        else:
            logger.warning(Fore.YELLOW + "No valid name found in the PDF for LinkedIn search." + Style.RESET_ALL)
            logger.info("Attempting to search recruiters on LinkedIn.")
            search_linkedin(["Recruiter", "Talent Acquisition"], companyname)
            return None
    except Exception as e:
        logger.error(Fore.RED + f"Error in LinkedIn search process: {e}" + Style.RESET_ALL)
        return None