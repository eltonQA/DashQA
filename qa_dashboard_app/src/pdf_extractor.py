
import PyPDF2
import pdfplumber
import tabula
from PIL import Image
import pytesseract
import os
from pdf2image import convert_from_path
import re
import sys

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() or ""
    return text

def extract_tables_from_pdf(pdf_path):
    tables = []
    
    # Try with pdfplumber first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        # Filter out empty rows/columns and ensure data integrity
                        cleaned_table = []
                        for row in table:
                            cleaned_row = [cell.replace('\n', ' ') if cell else '' for cell in row]
                            if any(cell.strip() for cell in cleaned_row):
                                cleaned_table.append(cleaned_row)
                        if cleaned_table:
                            tables.append(cleaned_table)
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    # Fallback to tabula-py if pdfplumber finds no tables or if it fails
    if not tables:
        try:
            # Ensure Java is in PATH or JAVA_HOME is set for tabula-py
            os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
            tables_tabula = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True, guess=False, lattice=True)
            for df in tables_tabula:
                tables.append(df.values.tolist())
        except Exception as e:
            print(f"Tabula-py failed as fallback: {e}")

    # If still no tables, try to parse from raw text for simple cases (like our example.pdf)
    if not tables:
        text_data = extract_text_from_pdf(pdf_path)
        lines = text_data.split('\n')
        status_data = []
        table_header_found = False
        for line in lines:
            line = line.strip()
            if re.match(r'Status\s*\|\s*Total', line, re.IGNORECASE):
                table_header_found = True
                status_data.append(["Status", "Total"])
                continue
            if table_header_found and re.search(r'(\w+)\s*\|\s*(\d+)', line):
                parts = re.findall(r'(\w+)\s*\|\s*(\d+)', line)
                for status, total in parts:
                    status_data.append([status, total])
            elif table_header_found and not line: 
                table_header_found = False

        if len(status_data) > 1: 
            tables.append(status_data)

    return tables

def ocr_pdf(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = f"page_{i}.png"
            image.save(image_path, 'PNG')
            text += pytesseract.image_to_string(Image.open(image_path))
            os.remove(image_path)
    except Exception as e:
        print(f"OCR failed: {e}. Ensure poppler-utils is installed and configured correctly.")
    return text

def extract_data_from_pdf(pdf_path):
    extracted_data = {
        "text": "",
        "tables": [],
        "ocr_text": ""
    }

    extracted_data["text"] = extract_text_from_pdf(pdf_path)
    extracted_data["tables"] = extract_tables_from_pdf(pdf_path)

    if not extracted_data["text"] and not extracted_data["tables"]:
        print("No text or tables found directly. Attempting OCR...")
        extracted_data["ocr_text"] = ocr_pdf(pdf_path)

    return extracted_data

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_to_process = sys.argv[1]
    else:
        pdf_to_process = "example.pdf"

    if not os.path.exists(pdf_to_process):
        print(f"Please place a PDF file named '{pdf_to_process}' in the current directory for testing.")
        print("You can also modify the 'pdf_to_process' variable to point to an existing PDF.")
    else:
        print(f"Extracting data from {pdf_to_process}...")
        data = extract_data_from_pdf(pdf_to_process)
        print("\n--- Extracted Text ---")
        print(data["text"])
        print("\n--- Extracted Tables ---")
        for i, table in enumerate(data["tables"]):
            print(f"Table {i+1}:\n{table}\n")
        print("\n--- Extracted OCR Text ---")
        print(data["ocr_text"])


