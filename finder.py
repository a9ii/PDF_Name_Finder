import os
import argparse
import unicodedata
from multiprocessing import Pool, cpu_count
import fitz  # Install via: pip install pymupdf
from tqdm import tqdm  # Install via: pip install tqdm
import re

# قائمة الأسماء المطلوب البحث عنها (أضيفت من بياناتك)
NAMES_TO_SEARCH = [
    "name1", 

    "name2" 
]

def extract_text_from_pdf(pdf_path):
    """استخراج النص من ملف PDF مع معالجة النصوص العربية"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text(flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE)
        return unicodedata.normalize('NFKC', text.strip())
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return ''

def search_in_pdf(pdf_info):
    """البحث عن الأسماء في ملف PDF مع تحديد الأسماء المطابقة"""
    pdf_path, names = pdf_info
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None

    text = text.replace('\n', ' ').replace('\t', ' ')
    text = ' '.join(text.split())
    
    matched_names = []
    for name in names:
        normalized_name = unicodedata.normalize('NFKC', name.strip())
        pattern = r'\b' + re.escape(normalized_name) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE | re.UNICODE):
            matched_names.append(name)
    
    return (pdf_path, matched_names) if matched_names else None

def get_pdf_files(directory):
    """جمع جميع ملفات PDF في المجلد وتحت مجلداته"""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def main():
    parser = argparse.ArgumentParser(description='Search for predefined names in PDF files and show matches')
    parser.add_argument('directory', help='Target directory path')
    args = parser.parse_args()

    # جمع الأسماء النشطة (غير الفارغة)
    active_names = [name.strip() for name in NAMES_TO_SEARCH if name.strip()]
    
    if not active_names:
        print("Error: No active names found! Please add names in the NAMES_TO_SEARCH list.")
        return

    if not os.path.isdir(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist!")
        return

    pdf_files = get_pdf_files(args.directory)
    total_files = len(pdf_files)
    if total_files == 0:
        print("No PDF files found in the specified directory.")
        return

    print(f"\nStarting scan of {total_files} PDF file(s) for {len(active_names)} names...\n")

    found_files = []
    try:
        with Pool(processes=cpu_count()) as pool:
            tasks = [(pdf, active_names) for pdf in pdf_files]
            
            with tqdm(total=total_files, desc="Processing", unit="file",
                      bar_format='{l_bar}{bar} | {n_fmt}/{total_fmt} | Elapsed: {elapsed} | Remaining: {remaining}') as pbar:
                
                for result in pool.imap_unordered(search_in_pdf, tasks):
                    if result:
                        file_path, matches = result
                        tqdm.write(f"🔍 Found in: {file_path}")
                        for name in matches:
                            tqdm.write(f"   ✅ {name}")
                        found_files.append((file_path, matches))
                    pbar.update(1)
                    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")

    print("\n" + "="*70)
    if found_files:
        print(f"📝 Summary Report ({len(found_files)} files with matches):\n")
        for file_path, matches in found_files:
            print(f"📁 File: {file_path}")
            print("   Matching names:")
            for name in matches:
                print(f"   - {name}")
            print("")
    else:
        print("❌ No matches found for any of the names.")

if __name__ == '__main__':
    main()
