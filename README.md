# PDF Name Finder

## Overview
**PDF Name Finder** is a Python script designed to search for predefined names within PDF files in a specified directory. It efficiently extracts text from PDFs and identifies occurrences of the given names using pattern matching.

## Features
- Extracts text from PDF files while preserving Arabic and Unicode text formatting.
- Supports multi-core processing for faster search operations.
- Displays a detailed summary of matched names and their corresponding PDF files.
- Uses `tqdm` progress bars for better user experience.

## Prerequisites
Ensure you have Python installed (>= 3.6) and install the required dependencies:
```sh
pip install pymupdf tqdm
```

## Usage
Run the script by specifying the directory containing the PDF files:
```sh
python finder.py /path/to/pdf/directory
```

## Configuration
Modify the `NAMES_TO_SEARCH` list in the script to include the names you want to search for:
```python
NAMES_TO_SEARCH = [
    "name1",
    "name2"
]
```

## Output
- The script scans all PDF files in the specified directory.
- It displays matched names along with the corresponding file paths.
- A final summary report is presented, listing all PDF files containing matches.

## Example Output
```
🔍 Found in: /path/to/pdf1.pdf
   ✅ name1
   ✅ name2

🔍 Found in: /path/to/pdf2.pdf
   ✅ name1

==============================
📝 Summary Report (2 files with matches):
📁 File: /path/to/pdf1.pdf
   Matching names:
   - name1
   - name2

📁 File: /path/to/pdf2.pdf
   Matching names:
   - name1
```

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.


