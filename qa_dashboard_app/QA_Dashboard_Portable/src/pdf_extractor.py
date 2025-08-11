import PyPDF2
import pdfplumber
import tabula
from PIL import Image
import pytesseract
import os
from pdf2image import convert_from_path
import re

def extract_text_from_pdf(pdf_path):
    """Extrai texto de todas as páginas de um arquivo PDF."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)  # Inicializa o leitor de PDF
            for page_num in range(len(reader.pages)):
                # Extrai texto de cada página, tratando casos em que o texto é None
                text += reader.pages[page_num].extract_text() or ""
    except Exception as e:
        print(f"Erro ao extrair texto com PyPDF2: {e}")
    return text

def extract_tables_from_pdf(pdf_path):
    """Extrai tabelas de um arquivo PDF usando diferentes métodos."""
    tables = []
    
    # Prioriza a extração de tabelas a partir do texto bruto para casos simples (como example.pdf)
    text_data = extract_text_from_pdf(pdf_path)
    
    # Usa regex para encontrar linhas no formato 'Status | Total' e dados associados
    match = re.search(r'Status\s*\|\s*Total(.*)', text_data, re.DOTALL | re.IGNORECASE)
    if match:
        table_content = match.group(1)  # Captura o conteúdo após o cabeçalho
        lines = table_content.split('\n')
        status_data = [["Status", "Total"]]  # Inicializa com o cabeçalho
        for line in lines:
            line = line.strip()
            # Procura por linhas no formato 'Palavra | Número'
            if re.search(r'(\w+)\s*\|\s*(\d+)', line):
                parts = re.findall(r'(\w+)\s*\|\s*(\d+)', line)
                for status, total in parts:
                    status_data.append([status, total])  # Adiciona dados válidos à tabela

        if len(status_data) > 1:  # Inclui a tabela apenas se houver dados além do cabeçalho
            tables.append(status_data)

    # Se nenhuma tabela for encontrada no texto, tenta usar pdfplumber
    if not tables:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()  # Extrai tabelas de cada página
                    if page_tables:
                        for table in page_tables:
                            # Filtra linhas com pelo menos uma célula não vazia
                            df = [row for row in table if any(cell.strip() if cell else '' for cell in row)]
                            if df:
                                tables.append(df)
        except Exception as e:
            print(f"Falha ao extrair tabelas com pdfplumber: {e}")

    # Se ainda não houver tabelas, tenta usar tabula-py como alternativa
    if not tables:
        try:
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True)
        except Exception as e:
            print(f"Falha ao extrair tabelas com tabula-py: {e}")

    return tables

def ocr_pdf(pdf_path):
    """Aplica OCR em um PDF para extrair texto de imagens ou PDFs digitalizados."""
    text = ""
    try:
        # Converte cada página do PDF em uma imagem
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = f"page_{i}.png"  # Salva a imagem temporariamente
            image.save(image_path, 'PNG')
            # Extrai texto da imagem usando pytesseract
            text += pytesseract.image_to_string(Image.open(image_path))
            os.remove(image_path)  # Remove a imagem temporária
    except Exception as e:
        print(f"Falha no OCR: {e}. Verifique se poppler-utils está instalado e configurado corretamente.")
    return text

def extract_data_from_pdf(pdf_path):
    """Extrai texto, tabelas e texto OCR de um arquivo PDF."""
    # Inicializa dicionário para armazenar os dados extraídos
    extracted_data = {
        "text": "",
        "tables": [],
        "ocr_text": ""
    }

    # Extrai texto e tabelas usando as funções específicas
    extracted_data["text"] = extract_text_from_pdf(pdf_path)
    extracted_data["tables"] = extract_tables_from_pdf(pdf_path)

    # Se nenhum texto ou tabela for extraído, tenta OCR como última alternativa
    if not extracted_data["text"] and not extracted_data["tables"]:
        print("Nenhum texto ou tabela encontrado diretamente. Tentando OCR...")
        extracted_data["ocr_text"] = ocr_pdf(pdf_path)

    return extracted_data

if __name__ == "__main__":
    # Bloco para teste independente do extrator de PDF
    dummy_pdf_path = "example.pdf"
    if not os.path.exists(dummy_pdf_path):
        # Verifica se o arquivo PDF de teste existe no diretório atual
        print(f"Coloque um arquivo PDF chamado '{dummy_pdf_path}' no diretório atual para teste.")
        print("Você também pode modificar a variável 'dummy_pdf_path' para apontar para um PDF existente.")
    else:
        # Processa o PDF e exibe os dados extraídos
        print(f"Extraindo dados de {dummy_pdf_path}...")
        data = extract_data_from_pdf(dummy_pdf_path)
        print("\n--- Texto Extraído ---")
        print(data["text"])
        print("\n--- Tabelas Extraídas ---")
        for i, table in enumerate(data["tables"]):
            print(f"Tabela {i+1}:\n{table}\n")
        print("\n--- Texto Extraído via OCR ---")
        print(data["ocr_text"])