import os
import re
from typing import Dict


# Function to create a dictionary of PDF files with a numeric prefix
def filenames_and_prefix_from_dir(directory: str) -> Dict[str, str]:
    pdf_dict: Dict[str, str] = {}

    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        # Use regex to match the first four digits in the filename
        match = re.match(r"^(\d{4})", filename)

        # If the file is a PDF and the regex match is successful, add it to the dictionary
        if filename.endswith(".pdf") and match:
            pdf_dict[filename] = match.group(1)

    # Return the dictionary
    return pdf_dict


if __name__ == "__main__":
    # Specify the directory path
    directory_path: str = "pdf_files"

    # Create the dictionary of PDF files
    pdf_dict: Dict[str, str] = filenames_and_prefix_from_dir(directory_path)

    # Print the dictionary
    print("Dictionary der PDF-Dateien mit Präfix:")
    for filename, prefix in pdf_dict.items():
        print(f"{filename}: {prefix}")
