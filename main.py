import os
from PyPDF2 import PdfReader, PdfWriter
import spacy
import datetime
import re
import webbrowser
import asyncio
import logging
from colorama import Fore, Style
from Utils import Logging 
from Utils.LinkedInSearcher import extract_name_from_pdf, search_linkedin, main_linkedin_search
from Utils.MiscUtils import find_most_recent_pdf
from Utils.DocumentMerger import merge_pdfs, main_merger
from Utils.ChartMaker import read_pdfs_and_prepare_chart, prepare_chart_data, generate_chart, main_chart




async def run_main_merger(path_CoverLetters, path_LOR):
    """
    Wrapper to run the main_merger function asynchronously.
    """
    await asyncio.to_thread(main_merger, path_CoverLetters, path_LOR)

async def run_main_chart(path_CoverLetters):
    """
    Wrapper to run the main_chart function asynchronously.
    """
    await asyncio.to_thread(main_chart, path_CoverLetters)

async def run_main_linkedin_search(path_CoverLetters):
    """
    Wrapper to run the main_linkedin_search function asynchronously.
    """
    await asyncio.to_thread(main_linkedin_search, path_CoverLetters)

async def main():
    # Paths
    path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"

    # Run all tasks concurrently
    await asyncio.gather(
        run_main_merger(path_CoverLetters, path_LOR),
        run_main_linkedin_search(path_CoverLetters)
    )
    main_chart(path_CoverLetters)

def sync_main():
    path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"

    main_merger(path_CoverLetters, path_LOR)
    main_linkedin_search(path_CoverLetters)
    main_chart(path_CoverLetters)

if __name__ == "__main__":
    
    start_time = datetime.datetime.now()
    print(f"Starting at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    #sync_main()
    end_time = datetime.datetime.now()
    print("Execution completed.")
    # print duration in minutes and seconds
    duration = end_time - start_time
    print(f"Total execution time: {duration.seconds} seconds")
    logging.info(Fore.GREEN + f"Total execution time: {duration.seconds} seconds" + Style.RESET_ALL)



