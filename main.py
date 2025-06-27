print("Starting the main script...")
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import datetime
import asyncio
from colorama import Fore, Style
import logging
from Utils.Logging import logger  # Import the logger from your Logging module
from Utils.DocumentMerger import main_merger
from Utils.ChartMaker import main_chart
from Utils.LinkedInSearcher import main_linkedin_search
from Utils.LinkedInMessager import main_copymessage

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
    return await asyncio.to_thread(main_linkedin_search, path_CoverLetters)

async def main():
    # Paths
    path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"
    path_LinkedInMessage = r"LinkedInMessage.txt"
    logger.info("Running in asynchronous mode")
    # Run all tasks concurrently
    results = await asyncio.gather(
        run_main_merger(path_CoverLetters, path_LOR),
        run_main_linkedin_search(path_CoverLetters)
    )
    _, (name, company) = results
    main_copymessage(path_LinkedInMessage, name, company)
    main_chart(path_CoverLetters)

def sync_main():
    path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"
    path_LinkedInMessage = r"LinkedInMessage.txt"
    logger.info("Running in synchronous mode")
    
    main_merger(path_CoverLetters, path_LOR)
    name = main_linkedin_search(path_CoverLetters)
    if name is not None:
        main_copymessage(path_LinkedInMessage, name)
    main_chart(path_CoverLetters)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Current working directory: {os.getcwd()}")
    start_time = datetime.datetime.now()
    print(f"Starting at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Starting at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("Starting the main script successfully ...")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    # sync_main()
    logger.info("Ending the main script successfully ...")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print("Execution completed.")
    print(f"Total execution time: {duration.seconds} seconds")
    logger.info(f"Total execution time: {duration.seconds} seconds")



