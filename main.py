import os
from PyPDF2 import PdfReader, PdfWriter
import datetime
path_LOR = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf"
path_CoverLetters = r"D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass"

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

# function to read all pdfs and prepare a bar chart based on their creation dates
def read_pdfs_and_prepare_chart(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the directory.")
    
    creation_dates = []
    for pdf_file in pdf_files:
        file_path = os.path.join(directory, pdf_file)
        creation_time = os.path.getmtime(file_path)
        # Convert creation time to a readable format (optional)
        creation_date = datetime.datetime.fromtimestamp(creation_time)
        creation_date = creation_date.date()  
        str_creation_date = creation_date.strftime('%d-%m-%Y')
        creation_dates.append((pdf_file, str_creation_date))
    
    # Sort by creation date and month
    creation_dates.sort(key=lambda x: datetime.datetime.strptime(x[1], '%d-%m-%Y'))    
    
    # Prepare data for chart (this part can be customized based on charting library)
    return creation_dates

def prepare_chart_data(creation_dates):
    chart_data = {
        'labels': [],
        'values': []
    }
    count = {}
    for pdf_file, creation_date in creation_dates:
        if creation_date not in count:
            count[creation_date] = 0
        count[creation_date] += 1
    for date, value in count.items():
        chart_data['labels'].append(date)
        chart_data['values'].append(value)

    return chart_data

def generate_chart(chart_data):
    # This function can be customized to generate a chart using a specific library
    # For example, using matplotlib or any other charting library
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(10, 5))
    plt.bar(chart_data['labels'], chart_data['values'], color='blue')
    plt.xlabel('Creation Date')
    plt.ylabel('Number of PDFs')
    # difference between last and second last
    difference = chart_data['values'][-1] - chart_data['values'][-2] if len(chart_data['values']) > 1 else 0
    plt.title(f'Difference: {difference}')
    if difference < 0:
        today = datetime.date.today().strftime('%d.%m.%Y')
        plt.title(f"Number of Applications remaining today ({today}): {abs(difference)}")
    else:
        plt.title(f"Number of Applications additional applications done today: {abs(difference)}")
    for i, value in enumerate(chart_data['values']):
        plt.text(i, value + 0.1, str(value), ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right')
    # trendline
    z = np.polyfit(range(len(chart_data['values'])), chart_data['values'], 1)
    p = np.poly1d(z)
    plt.plot(chart_data['labels'], p(range(len(chart_data['values']))), color='red', linestyle='--', label='Trendline')
    plt.legend()
    plt.grid(axis='y')

    plt.tight_layout()
    plt.show()

def main_merger():
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
        print(f"Merged PDF saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main_chart():
    try:
        creation_dates = read_pdfs_and_prepare_chart(path_CoverLetters)
        chart_data = prepare_chart_data(creation_dates)
        generate_chart(chart_data)
    except Exception as e:
        print(f"An error occurred while preparing chart data: {e}")

if __name__ == "__main__":
    # Main logic

    main_merger()
    main_chart()