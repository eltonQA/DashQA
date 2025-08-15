# QA Dashboard App

Aplicativo para análise automatizada de métricas de Quality Assurance (QA) a partir de arquivos PDF.

🚀 Características Principais
📊 Dashboard Interativo: Interface web moderna com visualizações em tempo real.

📄 Extração Robusta: Suporte a múltiplas técnicas de extração de PDF, incluindo PyPDF2, pdfplumber e tabula-py.

⏰ Processamento Automático: Agendamento e monitoramento de pastas.

📈 KPIs Automáticos: Cálculo automático de métricas de QA, como total de casos de teste, casos passados, percentual de execução e percentual de sucesso.

💾 Exportação: Dados exportáveis em formato CSV.

🔍 OCR: Suporte a PDFs escaneados com Tesseract.

🤖 Geração de Relatórios com IA: Criação de resumos profissionais para plataformas como o Microsoft Teams, utilizando a API Gemini da Google.

🛠️ Tecnologias Utilizadas
Python 3.8+: Linguagem principal.

Streamlit: Interface web interativa.

Plotly: Visualizações e gráficos.

pandas: Processamento de dados.

PyPDF2/pdfplumber/tabula-py: Extração de PDFs.

Tesseract OCR: Reconhecimento óptico de caracteres.

Google Gemini API: Geração de texto com IA.

📦 Instalação Rápida
Método 1: Pacote Portável
Baixe o pacote QA_Dashboard_Portable.

Execute Instalar_Dependencias.bat (Windows).

Use Iniciar_Dashboard.bat para começar.

Método 2: Instalação Manual
Bash

# Clone o repositório
git clone <repository-url>
cd qa_dashboard_app

# Instale dependências
pip install -r requirements.txt

# Execute o aplicativo
python app.py
🎯 Como Usar
Dashboard Interativo
Bash

python app.py dashboard
Acesse http://localhost:8501.

Faça upload de PDFs via interface.

Visualize métricas automaticamente.

Exporte dados em CSV.

Gere resumos de IA para Teams.

Processamento Automático
Bash

python app.py scheduler
Coloque PDFs na pasta input_pdfs/.

O processamento diário automático ocorre às 09:00.

Os arquivos CSVs gerados são salvos em processed_data/.

Teste Rápido
Bash

python app.py test
Realiza um teste de processamento de PDFs.

📁 Estrutura do Projeto
qa_dashboard_app/
├── app.py                    # Script principal
├── dashboard.py              # Interface Streamlit e lógica do dashboard
├── scheduler.py              # Agendador automático
├── src/
│   ├── pdf_extractor.py      # Extração de PDFs
│   └── data_processor.py     # Processamento de dados
├── docs/                     # Documentação
├── input_pdfs/               # Pasta de entrada
└── processed_data/           # Pasta de saída
📊 Métricas Suportadas
O aplicativo extrai e calcula automaticamente as seguintes métricas a partir dos PDFs:

Total de Casos de Teste

Casos Passados/Falhados/Bloqueados

Percentual de Execução

Percentual de Sucesso

Distribuição por Status

🔧 Requisitos do Sistema
Obrigatórios
Python 3.8+.

Java Runtime Environment (para tabula-py).

Opcionais
Tesseract OCR (para PDFs escaneados).

poppler-utils (para conversão PDF→imagem).

📖 Documentação
Manual do Usuário.

Documentação Técnica.

🐛 Solução de Problemas
Java não encontrado
Bash

# Ubuntu/Debian
sudo apt-get install openjdk-11-jre

# Windows
# Baixe e instale Java JRE
Tesseract não encontrado
Bash

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Baixe do GitHub oficial do Tesseract
🤝 Contribuição
Fork o projeto.

Crie uma branch para sua feature.

Commit suas mudanças.

Push para a branch.

Abra um Pull Request.

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

🆘 Suporte
Para problemas ou dúvidas:

Consulte a documentação em docs/.

Verifique issues existentes.

Abra uma nova issue se necessário.

Desenvolvido com ❤️ para automatizar análises de QA
