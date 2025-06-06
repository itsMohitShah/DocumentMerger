# Document Merger

This Python script automates the process of merging the most recent PDF file from a specified directory of cover letters with a specified Letter of Recommendation (LOR) PDF file. The merged file is saved in the parent directory of the cover letters folder with an updated name.

## Features

- Automatically identifies the most recent PDF file in the cover letters directory.
- Merges the selected cover letter PDF with the specified LOR PDF.
- Updates the name of the merged file by replacing "Cover Letter" with "Cover Letter with LOR" in the original file name.
- Saves the merged file in the parent directory of the cover letters folder.

## Requirements

- Python 3.6 or higher
- `PyPDF2` library

## Installation

1. Clone or download this repository.
2. Install the required Python library using pip:

   ```bash
   pip install PyPDF2

## Usage
1. Update the paths in the script:

    - path_LOR: Path to the LOR PDF file.
    - path_CoverLetters: Path to the directory containing cover letter PDFs.
2. Run the script:
    ```bash
    python main.py

3. The merged PDF will be saved in the parent directory of the cover letters folder with the updated name.

## Example

Input:
- Cover letter directory: D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters\FromEuroPass
- LOR file: D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\LOR - NIDO 2020.pdf

Output:
- Merged file saved in: D:\OneDrive - Students RWTH Aachen University\User Data\Mohitto Laptop\Mohitto\Resume\Cover Letters
- File name: Cover Letter with LOR.pdf (if the original file name contains "Cover Letter").

## Error Handling
- If no PDF files are found in the cover letters directory, the script raises a FileNotFoundError.
- Any other exceptions are caught and displayed in the console.

## License
This project is licensed under the MIT License. 