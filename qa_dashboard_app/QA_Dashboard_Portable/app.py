#!/usr/bin/env python3
"""
QA Dashboard App - Aplicativo para análise de métricas de QA a partir de PDFs
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

VENV_DIR = "venv"

def which_python_executable():
    """Retorna python do sistema (sys.executable)."""
    return sys.executable

def venv_python(venv_dir):
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")

def create_venv(venv_dir):
    print(f"🔧 Criando virtualenv em ./{venv_dir} ...")
    subprocess.check_call([which_python_executable(), "-m", "venv", venv_dir])
    print("✅ Virtualenv criado.")

def pip_install(venv_py, requirements_file=None, packages=None):
    # upgrade pip/setuptools first
    print("⬆️  Atualizando pip, setuptools e wheel no venv...")
    subprocess.check_call([venv_py, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    if requirements_file and os.path.isfile(requirements_file):
        print(f"📥 Instalando dependências de {requirements_file} ...")
        subprocess.check_call([venv_py, "-m", "pip", "install", "-r", requirements_file])
    elif packages:
        print(f"📥 Instalando pacotes: {packages} ...")
        subprocess.check_call([venv_py, "-m", "pip", "install"] + packages)

def start_streamlit_with_venv(venv_py, target="dashboard.py"):
    print("🚀 Iniciando Streamlit pelo Python do venv...")
    try:
        subprocess.run([venv_py, "-m", "streamlit", "run", target], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar o Streamlit: {e}")
    except Exception as e:
        print(f"❌ Exceção inesperada: {e}")

def main():
    if len(sys.argv) <= 1 or sys.argv[1].lower() != "dashboard":
        print("📌 Uso: python app.py dashboard")
        sys.exit(0)

    # 1) criar venv se não existir
    if not os.path.isdir(VENV_DIR):
        try:
            create_venv(VENV_DIR)
        except subprocess.CalledProcessError as e:
            print("❌ Falha ao criar virtualenv:", e)
            sys.exit(1)

    # 2) caminho para python do venv
    vpy = venv_python(VENV_DIR)
    if not os.path.isfile(vpy):
        print(f"❌ Python do venv não encontrado em {vpy}")
        sys.exit(1)

    # 3) instalar dependências dentro do venv
    try:
        requirements = "requirements.txt"
        if os.path.isfile(requirements):
            pip_install(vpy, requirements_file=requirements)
        else:
            # dependências mínimas caso não tenha requirements.txt
            pip_install(vpy, packages=["streamlit", "pandas", "matplotlib", "numpy", "plotly", "python-dateutil"])
    except subprocess.CalledProcessError as e:
        print("❌ Falha ao instalar dependências dentro do venv:", e)
        print("Tente inspecionar o erro acima ou rodar manualmente:")
        print(f"  {vpy} -m pip install -r requirements.txt")
        sys.exit(1)

    # 4) iniciar o dashboard
    start_streamlit_with_venv(vpy, target="dashboard.py")

if __name__ == "__main__":
    main()
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

