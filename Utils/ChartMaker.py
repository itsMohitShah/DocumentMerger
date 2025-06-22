import os
import datetime
import matplotlib.pyplot as plt
import matplotlib

import numpy as np
import logging
from colorama import Fore, Style

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to read all PDFs and prepare a bar chart based on their creation dates
def read_pdfs_and_prepare_chart(directory):
    try:
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("No PDF files found in the directory.")
        
        creation_dates = []
        for pdf_file in pdf_files:
            file_path = os.path.join(directory, pdf_file)
            creation_time = os.path.getmtime(file_path)
            creation_date = datetime.datetime.fromtimestamp(creation_time).date()
            str_creation_date = creation_date.strftime('%d-%m-%Y')
            creation_dates.append((pdf_file, str_creation_date))
        
        # Sort by creation date
        creation_dates.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))
        logging.info(Fore.GREEN + f"Successfully read and prepared creation dates for {len(pdf_files)} PDFs." + Style.RESET_ALL)
        return creation_dates
    except Exception as e:
        logging.error(Fore.RED + f"Error reading PDFs and preparing chart data: {e}" + Style.RESET_ALL)
        raise

# Function to prepare chart data
def prepare_chart_data(creation_dates):
    try:
        chart_data = {
            'labels': [],
            'values': []
        }
        count = {}
        for _, creation_date in creation_dates:
            if creation_date not in count:
                count[creation_date] = 0
            count[creation_date] += 1
        for date, value in count.items():
            chart_data['labels'].append(date)
            chart_data['values'].append(value)

        logging.info(Fore.GREEN + "Chart data prepared successfully." + Style.RESET_ALL)
        return chart_data
    except Exception as e:
        logging.error(Fore.RED + f"Error preparing chart data: {e}" + Style.RESET_ALL)
        raise

# Function to generate the chart
def generate_chart(chart_data):
    try:
        plt.figure(figsize=(10, 5))
        plt.bar(chart_data['labels'], chart_data['values'], color='blue')
        plt.xlabel('Creation Date')
        plt.ylabel('Number of PDFs')

        # Calculate the difference between the last and second last values
        difference = chart_data['values'][-1] - chart_data['values'][-2] if len(chart_data['values']) > 1 else 0
        today = datetime.date.today().strftime('%d.%m.%Y')
        if difference < 0:
            plt.title(f"Number of Applications remaining today ({today}): {abs(difference)}")
        else:
            plt.title(f"Number of additional applications done today: {abs(difference)}")

        # Add value labels to the bars
        for i, value in enumerate(chart_data['values']):
            plt.text(i, value + 0.1, str(value), ha='center', va='bottom')

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')

        # Add a trendline
        z = np.polyfit(range(len(chart_data['values'])), chart_data['values'], 1)
        p = np.poly1d(z)
        plt.plot(chart_data['labels'], p(range(len(chart_data['values']))), color='red', linestyle='--', label='Trendline')
        plt.legend()
        plt.grid(axis='y')

        plt.tight_layout()
        plt.show()
        logging.info(Fore.GREEN + "Chart generated and displayed successfully." + Style.RESET_ALL)
    except Exception as e:
        logging.error(Fore.RED + f"Error generating chart: {e}" + Style.RESET_ALL)

# Main function to handle the chart creation process
def main_chart(path_CoverLetters):
    try:
        creation_dates = read_pdfs_and_prepare_chart(path_CoverLetters)
        chart_data = prepare_chart_data(creation_dates)
        generate_chart(chart_data)
        logging.info(Fore.GREEN + "Chart creation process completed successfully." + Style.RESET_ALL)
    except Exception as e:
        logging.error(Fore.RED + f"An error occurred while preparing chart data: {e}" + Style.RESET_ALL)