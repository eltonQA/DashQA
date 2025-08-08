#!/usr/bin/env python3
"""
Script de build para criar executável do QA Dashboard App
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_executable():
    """Cria o executável usando PyInstaller"""
    print("Criando executável do QA Dashboard App...")
    
    # Ensure we're in the app directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "QA_Dashboard_App",
        "--add-data", "src;src",
        "--add-data", "dashboard.py;.",
        "--add-data", "scheduler.py;.",
        "--hidden-import", "streamlit",
        "--hidden-import", "plotly",
        "--hidden-import", "pandas",
        "--hidden-import", "PyPDF2",
        "--hidden-import", "pdfplumber",
        "--hidden-import", "tabula",
        "--hidden-import", "pytesseract",
        "--hidden-import", "PIL",
        "--hidden-import", "pdf2image",
        "--hidden-import", "schedule",
        "app.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Executável criado com sucesso!")
        print("✓ Arquivo: dist/QA_Dashboard_App.exe")
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao criar executável: {e}")
        return False
    
    return True

def create_portable_package():
    """Cria um pacote portável com todas as dependências"""
    print("Criando pacote portável...")
    
    package_dir = Path("QA_Dashboard_Portable")
    
    # Remove existing package directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    # Create package structure
    package_dir.mkdir()
    (package_dir / "data").mkdir()
    (package_dir / "input_pdfs").mkdir()
    (package_dir / "processed_data").mkdir()
    (package_dir / "input_pdfs" / "processed").mkdir()
    
    # Copy executable if it exists
    exe_path = Path("dist/QA_Dashboard_App.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir / "QA_Dashboard_App.exe")
    
    # Copy Python files for non-executable usage
    files_to_copy = [
        "app.py",
        "dashboard.py", 
        "scheduler.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, package_dir / file)
    
    # Copy src directory
    if Path("src").exists():
        shutil.copytree("src", package_dir / "src")
    
    # Create batch files for Windows
    create_batch_files(package_dir)
    
    # Create README for the package
    create_package_readme(package_dir)
    
    print(f"✓ Pacote portável criado: {package_dir}")
    return True

def create_batch_files(package_dir):
    """Cria arquivos batch para facilitar o uso no Windows"""
    
    # Dashboard launcher
    dashboard_bat = package_dir / "Iniciar_Dashboard.bat"
    dashboard_bat.write_text("""@echo off
echo Iniciando QA Dashboard...
python app.py dashboard
pause
""")
    
    # Scheduler launcher
    scheduler_bat = package_dir / "Iniciar_Agendador.bat"
    scheduler_bat.write_text("""@echo off
echo Iniciando Agendador Automatico...
python app.py scheduler
pause
""")
    
    # Test launcher
    test_bat = package_dir / "Testar_Processamento.bat"
    test_bat.write_text("""@echo off
echo Testando processamento de PDFs...
python app.py test
pause
""")
    
    # Install requirements
    install_bat = package_dir / "Instalar_Dependencias.bat"
    install_bat.write_text("""@echo off
echo Instalando dependencias Python...
pip install -r requirements.txt
echo.
echo Instalacao concluida!
pause
""")

def create_package_readme(package_dir):
    """Cria README para o pacote"""
    readme_content = """# QA Dashboard App - Pacote Portável

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Java (para tabula-py)
- Tesseract OCR (opcional, para PDFs escaneados)

### Instalação das Dependências
1. Execute `Instalar_Dependencias.bat` ou
2. Execute manualmente: `pip install -r requirements.txt`

## Como Usar

### Opção 1: Executável (se disponível)
- Execute `QA_Dashboard_App.exe`

### Opção 2: Scripts Python
- **Dashboard Interativo**: Execute `Iniciar_Dashboard.bat` ou `python app.py dashboard`
- **Agendador Automático**: Execute `Iniciar_Agendador.bat` ou `python app.py scheduler`
- **Teste de Processamento**: Execute `Testar_Processamento.bat` ou `python app.py test`

## Estrutura de Pastas

```
QA_Dashboard_Portable/
├── QA_Dashboard_App.exe     # Executável (se disponível)
├── app.py                   # Script principal
├── dashboard.py             # Dashboard Streamlit
├── scheduler.py             # Agendador automático
├── src/                     # Módulos de processamento
├── input_pdfs/              # Coloque PDFs aqui para processamento automático
├── processed_data/          # CSVs processados são salvos aqui
└── input_pdfs/processed/    # PDFs processados são movidos para aqui
```

## Funcionalidades

✓ **Dashboard Interativo**
  - Upload de PDFs via interface web
  - Visualização de KPIs e gráficos
  - Exportação para CSV

✓ **Processamento Automático**
  - Agendamento diário de processamento
  - Monitoramento de pasta de entrada
  - Processamento em lote

✓ **Extração Robusta**
  - Múltiplas técnicas de extração (PyPDF2, pdfplumber, tabula-py)
  - Suporte a OCR para PDFs escaneados
  - Fallback automático entre métodos

## Suporte

Para problemas ou dúvidas, consulte a documentação completa no arquivo README.md principal.
"""
    
    (package_dir / "LEIA-ME.txt").write_text(readme_content, encoding='utf-8')

def main():
    """Função principal do script de build"""
    print("=== QA Dashboard App - Script de Build ===")
    
    # Create executable
    if "--exe" in sys.argv or "--all" in sys.argv:
        if not create_executable():
            print("Falha ao criar executável, continuando com pacote portável...")
    
    # Create portable package
    if "--package" in sys.argv or "--all" in sys.argv or len(sys.argv) == 1:
        create_portable_package()
    
    print("\n=== Build Concluído ===")
    print("Arquivos gerados:")
    if Path("dist/QA_Dashboard_App.exe").exists():
        print("  - dist/QA_Dashboard_App.exe")
    if Path("QA_Dashboard_Portable").exists():
        print("  - QA_Dashboard_Portable/ (pacote completo)")

if __name__ == "__main__":
    main()

