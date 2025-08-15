# QA Dashboard App

Aplicativo para análise automatizada de métricas de Quality Assurance (QA) a partir de arquivos PDF.

## 🚀 Características Principais

- **📊 Dashboard Interativo**: Interface web moderna com visualizações em tempo real
- **📄 Extração Robusta**: Suporte a múltiplas técnicas de extração de PDF
- **⏰ Processamento Automático**: Agendamento e monitoramento de pastas
- **📈 KPIs Automáticos**: Cálculo automático de métricas de QA
- **💾 Exportação**: Dados exportáveis em formato CSV
- **🔍 OCR**: Suporte a PDFs escaneados com Tesseract

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Streamlit**: Interface web interativa
- **Plotly**: Visualizações e gráficos
- **pandas**: Processamento de dados
- **PyPDF2/pdfplumber/tabula-py**: Extração de PDFs
- **Tesseract OCR**: Reconhecimento óptico de caracteres

## 📦 Instalação Rápida

### Método 1: Pacote Portável
1. Baixe o pacote `QA_Dashboard_Portable`
2. Execute `Instalar_Dependencias.bat` (Windows)
3. Use `Iniciar_Dashboard.bat` para começar

### Método 2: Instalação Manual
```bash
# Clone o repositório
git clone <repository-url>
cd qa_dashboard_app

# Instale dependências
pip install -r requirements.txt

# Execute o aplicativo
python app.py
```

## 🎯 Como Usar

### Dashboard Interativo
```bash
python app.py dashboard
```
- Acesse http://localhost:8501
- Faça upload de PDFs via interface
- Visualize métricas automaticamente
- Exporte dados em CSV

### Processamento Automático
```bash
python app.py scheduler
```
- Coloque PDFs na pasta `input_pdfs/`
- Processamento diário automático às 09:00
- CSVs gerados em `processed_data/`

### Teste Rápido
```bash
python app.py test
```

## 📁 Estrutura do Projeto

```
qa_dashboard_app/
├── app.py                    # Script principal
├── dashboard.py              # Interface Streamlit
├── scheduler.py              # Agendador automático
├── src/
│   ├── pdf_extractor.py      # Extração de PDFs
│   └── data_processor.py     # Processamento de dados
├── docs/                     # Documentação
├── input_pdfs/               # Pasta de entrada
└── processed_data/           # Pasta de saída
```

## 📊 Métricas Suportadas

O aplicativo extrai e calcula automaticamente:

- **Total de Casos de Teste**
- **Casos Passados/Falhados/Bloqueados**
- **Percentual de Execução**
- **Percentual de Sucesso**
- **Distribuição por Status**

## 🔧 Requisitos do Sistema

### Obrigatórios
- Python 3.8+
- Java Runtime Environment (para tabula-py)

### Opcionais
- Tesseract OCR (para PDFs escaneados)
- poppler-utils (para conversão PDF→imagem)

## 📖 Documentação

- [Manual do Usuário](docs/Manual_Usuario.md)
- [Documentação Técnica](docs/Documentacao_Tecnica.md)

## 🐛 Solução de Problemas

### Java não encontrado
```bash
# Ubuntu/Debian
sudo apt-get install openjdk-11-jre

# Windows
# Baixe e instale Java JRE
```

### Tesseract não encontrado
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Baixe do GitHub oficial do Tesseract
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Consulte a documentação em `docs/`
2. Verifique issues existentes
3. Abra uma nova issue se necessário

---

**Desenvolvido com ❤️ para automatizar análises de QA**
