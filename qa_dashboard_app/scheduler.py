import schedule
import time
import os
import sys
from datetime import datetime
import shutil

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_extractor import extract_data_from_pdf
from data_processor import process_extracted_data

class QAScheduler:
    def __init__(self, input_folder="input_pdfs", output_folder="processed_data"):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.processed_folder = os.path.join(input_folder, "processed")
        
        # Create directories if they don't exist
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
    
    def process_pdfs(self):
        """Process all PDFs in the input folder"""
        print(f"[{datetime.now()}] Iniciando processamento automático de PDFs...")
        
        pdf_files = [f for f in os.listdir(self.input_folder) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"[{datetime.now()}] Nenhum arquivo PDF encontrado na pasta {self.input_folder}")
            return
        
        for pdf_file in pdf_files:
            try:
                pdf_path = os.path.join(self.input_folder, pdf_file)
                print(f"[{datetime.now()}] Processando {pdf_file}...")
                
                # Extract data from PDF
                extracted_data = extract_data_from_pdf(pdf_path)
                processed_data = process_extracted_data(extracted_data)
                
                # Save processed data as CSV
                if not processed_data["df_status"].empty:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    csv_filename = f"qa_metrics_{timestamp}_{pdf_file.replace('.pdf', '.csv')}"
                    csv_path = os.path.join(self.output_folder, csv_filename)
                    
                    processed_data["df_status"].to_csv(csv_path, index=False)
                    print(f"[{datetime.now()}] Dados salvos em {csv_path}")
                    
                    # Move processed PDF to processed folder
                    processed_pdf_path = os.path.join(self.processed_folder, pdf_file)
                    shutil.move(pdf_path, processed_pdf_path)
                    print(f"[{datetime.now()}] PDF movido para {processed_pdf_path}")
                else:
                    print(f"[{datetime.now()}] Erro: Não foi possível extrair dados válidos de {pdf_file}")
                    
            except Exception as e:
                print(f"[{datetime.now()}] Erro ao processar {pdf_file}: {str(e)}")
        
        print(f"[{datetime.now()}] Processamento automático concluído.")
    
    def start_scheduler(self, schedule_time="09:00"):
        """Start the scheduler to run daily at specified time"""
        print(f"Agendador iniciado. PDFs serão processados diariamente às {schedule_time}")
        print(f"Pasta de entrada: {os.path.abspath(self.input_folder)}")
        print(f"Pasta de saída: {os.path.abspath(self.output_folder)}")
        print("Pressione Ctrl+C para parar o agendador")
        
        schedule.every().day.at(schedule_time).do(self.process_pdfs)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nAgendador interrompido pelo usuário.")

if __name__ == "__main__":
    scheduler = QAScheduler()
    
    # For testing, process PDFs immediately
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        scheduler.process_pdfs()
    else:
        # Start the scheduler
        scheduler.start_scheduler()

