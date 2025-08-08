
import PyPDF2
import pdfplumber
import tabula
from PIL import Image
import pytesseract
import os
from pdf2image import convert_from_path
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() or ""
    return text

def extract_tables_from_pdf(pdf_path):
    tables = []
    
    # Prioritize parsing from raw text for simple cases (like our example.pdf)
    text_data = extract_text_from_pdf(pdf_path)
    
    # Regex to find lines like 'Status | Total' and then data rows like 'Passou | 100'
    # This regex is more specific to the example PDF format and handles concatenated lines
    match = re.search(r'Status\s*\|\s*Total(.*)', text_data, re.DOTALL | re.IGNORECASE)
    if match:
        table_content = match.group(1)
        lines = table_content.split('\n')
        status_data = []
        status_data.append(["Status", "Total"])
        for line in lines:
            line = line.strip()
            if re.search(r'(\w+)\s*\|\s*(\d+)', line):
                parts = re.findall(r'(\w+)\s*\|\s*(\d+)', line)
                for status, total in parts:
                    status_data.append([status, total])

        if len(status_data) > 1: 
            tables.append(status_data)

    # Fallback to pdfplumber and tabula-py for more complex PDFs if no tables found from text
    if not tables:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table in page_tables:
                            df = [row for row in table if any(cell.strip() if cell else '' for cell in row)]
                            if df:
                                tables.append(df)
        except Exception as e:
            print(f"pdfplumber failed: {e}")

    if not tables:
        try:
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True)
        except Exception as e:
            print(f"Tabula-py failed as fallback: {e}")

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
    dummy_pdf_path = "example.pdf"
    if not os.path.exists(dummy_pdf_path):
        print(f"Please place a PDF file named '{dummy_pdf_path}' in the current directory for testing.")
        print("You can also modify the 'dummy_pdf_path' variable to point to an existing PDF.")
    else:
        print(f"Extracting data from {dummy_pdf_path}...")
        data = extract_data_from_pdf(dummy_pdf_path)
        print("\n--- Extracted Text ---")
        print(data["text"])
        print("\n--- Extracted Tables ---")
        for i, table in enumerate(data["tables"]):
            print(f"Table {i+1}:\n{table}\n")
        print("\n--- Extracted OCR Text ---")
        print(data["ocr_text"])
