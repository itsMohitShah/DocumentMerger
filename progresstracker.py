import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from Utils.Logging import logger  # Import the logger from your Logging module
from Utils.ChartMaker import main_chart


if __name__ == "__main__":
    path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"
    logger.info("Starting the progress tracker...")
    try:
        main_chart(path_CoverLetters)
        logger.info("Progress tracker completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred in the progress tracker: {e}")
    finally:
        logger.info("Progress tracker finished.")