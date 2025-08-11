"""
QA Dashboard App - Aplicativo para análise de métricas de QA a partir de PDFs
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_dashboard():
    """Executa o dashboard Streamlit"""
    print("Iniciando QA Dashboard...")
    print("O dashboard será aberto no seu navegador padrão.")
    print("Pressione Ctrl+C para parar o aplicativo.")
    
    try:
        # Change to the app directory
        app_dir = Path(__file__).parent
        os.chdir(app_dir)
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\nAplicativo encerrado pelo usuário.")
    except Exception as e:
        print(f"Erro ao executar o dashboard: {e}")
def run_scheduler():
    """Executa o agendador de processamento automático"""
    print("Iniciando agendador de processamento automático...")
    
    try:
        # Change to the app directory
        app_dir = Path(__file__).parent
        os.chdir(app_dir)
        
        # Run scheduler
        subprocess.run([sys.executable, "scheduler.py"])
    except KeyboardInterrupt:
        print("\nAgendador encerrado pelo usuário.")
    except Exception as e:
        print(f"Erro ao executar o agendador: {e}")

def test_scheduler():
    """Testa o processamento de PDFs"""
    print("Testando processamento de PDFs...")
    
    try:
        # Change to the app directory
        app_dir = Path(__file__).parent
        os.chdir(app_dir)
        
        # Run scheduler in test mode
        subprocess.run([sys.executable, "scheduler.py", "--test"])
    except Exception as e:
        print(f"Erro ao testar o processamento: {e}")

def show_help():
    """Mostra informações de ajuda"""
    help_text = """
QA Dashboard App - Aplicativo para análise de métricas de QA

COMANDOS DISPONÍVEIS:
  dashboard    - Inicia o dashboard interativo (padrão)
  scheduler    - Inicia o agendador de processamento automático
  test         - Testa o processamento de PDFs
  help         - Mostra esta ajuda

EXEMPLOS DE USO:
  python app.py                    # Inicia o dashboard
  python app.py dashboard          # Inicia o dashboard
  python app.py scheduler          # Inicia o agendador
  python app.py test               # Testa o processamento

ESTRUTURA DE PASTAS:
  input_pdfs/          - Coloque os PDFs aqui para processamento automático
  processed_data/      - CSVs processados são salvos aqui
  input_pdfs/processed/- PDFs processados são movidos para aqui

FUNCIONALIDADES:
  ✓ Upload e análise de PDFs com métricas de QA
  ✓ Dashboard interativo com gráficos e KPIs
  ✓ Exportação de dados para CSV
  ✓ Processamento automático agendado
  ✓ Extração de tabelas usando múltiplas técnicas
  ✓ Suporte a OCR para PDFs escaneados
"""
    print(help_text)

def main():
    """Função principal do aplicativo"""
    parser = argparse.ArgumentParser(
        description="QA Dashboard App - Aplicativo para análise de métricas de QA",
      add_help=False
    )
    parser.add_argument(
        'command', 
        nargs='?', 
        default='dashboard',
        choices=['dashboard', 'scheduler', 'test', 'help'],
        help='Comando a ser executado'
    )
    
    args = parser.parse_args()
    
    if args.command == 'dashboard':
        run_dashboard()
    elif args.command == 'scheduler':
        run_scheduler()
    elif args.command == 'test':
        test_scheduler()
    elif args.command == 'help':
        show_help()

if __name__ == "__main__":
    main()