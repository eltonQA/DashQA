import pandas as pd

def process_extracted_data(extracted_data):
    # Inicializa DataFrame vazio para armazenar contagem de status
    df_status = pd.DataFrame()
    # Dicionário para armazenar KPIs calculados
    kpis = {}
    # DataFrame vazio como placeholder para dados agrupados (não utilizado no momento)
    grouped_data = pd.DataFrame()

    # Extrai tabelas e texto dos dados fornecidos
    tables = extracted_data["tables"]
    text_data = extracted_data["text"]

    # Lista de palavras-chave para identificar status de testes
    status_keywords = ["Passou", "Falhado", "Bloqueado", "Não Executado"]
    # Inicializa contadores para cada status
    status_counts = {keyword: 0 for keyword in status_keywords}

    # Busca dados de status nas tabelas primeiro
    for table in tables:
        for row in table:
            for cell in row:
                if cell:  # Verifica se a célula não está vazia
                    for keyword in status_keywords:
                        # Conta ocorrências de cada status (case-insensitive)
                        if keyword.lower() in cell.lower():
                            status_counts[keyword] += 1

    # Converte contagem de status em DataFrame, incluindo apenas status com contagem maior que zero
    if any(status_counts.values()):
        df_status = pd.DataFrame(list(status_counts.items()), columns=["Status", "Total"])
        df_status = df_status[df_status["Total"] > 0]
    else:
        # Caso não sejam encontrados dados nas tabelas, tenta extrair de texto (formato 'example.pdf')
        lines = text_data.split("\n")
        status_data = []
        table_header_found = False
        for line in lines:
            line = line.strip()
            # Identifica o cabeçalho da tabela no texto
            if "Status | Total" in line:
                table_header_found = True
                continue
            if table_header_found and line:
                parts = line.split("|")
                if len(parts) == 2:  # Verifica se a linha tem o formato esperado
                    status = parts[0].strip()
                    try:
                        total = int(parts[1].strip())
                        status_data.append([status, total])
                    except ValueError:
                        pass  # Ignora linhas onde 'Total' não é um número
        if status_data:
            df_status = pd.DataFrame(status_data, columns=["Status", "Total"])

    # Calcula KPIs se o DataFrame de status não estiver vazio
    if not df_status.empty:
        total_cases = df_status["Total"].sum()  # Total de casos de teste
        passed_cases = df_status[df_status["Status"].str.contains("Passou", case=False)]["Total"].sum()  # Casos que passaram
        executed_cases = df_status[~df_status["Status"].str.contains("Não Executado", case=False)]["Total"].sum()  # Casos executados

        # Calcula percentual de execução (casos executados / total de casos)
        percent_execution = (executed_cases / total_cases) * 100 if total_cases > 0 else 0
        # Calcula percentual de sucesso (casos que passaram / casos executados)
        percent_success = (passed_cases / executed_cases) * 100 if executed_cases > 0 else 0

        # Armazena KPIs em um dicionário
        kpis = {
            "Total de Casos de Teste": total_cases,
            "Casos Passados": passed_cases,
            "Casos Executados": executed_cases,
            "Percentual de Execução": percent_execution,
            "Percentual de Sucesso": percent_success
        }

    # Retorna dicionário com DataFrame de status, KPIs e dados agrupados
    return {
        "df_status": df_status,
        "kpis": kpis,
        "grouped_data": grouped_data
    }

if __name__ == "__main__":
    # Bloco para teste independente da função process_extracted_data
    # Simula dados extraídos para testar a funcionalidade
    sample_extracted_data = {
        "text": "",
        "tables": [
            # Estrutura de tabela simulada baseada no formato TestLink1.9.20[fixed].pdf
            [
                ["#:", "Ações do Passo:", "Resultados Esperados::", "Estado da\nExecução:"],
                ["1", "Dado que o usuário sincroniza os pedidos\nQuando o usuário entra na tela de “Meus\npedidos”", "Então o banner aparece conforme\nfigma.", "Passou"]
            ],
            # Tabela adicional com 'Resultado da Execução'
            [
                ["Build", "SP49_C1", None, None],
                ["Testador", "mateus.sandes", None, None],
                ["Resultado da Execução:", "Falhado", None, None],
                ["Modo de Execução:", "Manual", None, None]
            ]
        ],
        "ocr_text": ""
    }

    # Processa os dados simulados e exibe resultados
    processed_data = process_extracted_data(sample_extracted_data)
    print("--- Dados de Status Processados ---")
    print(processed_data["df_status"])
    print("--- KPIs Calculados ---")
    print(processed_data["kpis"])

    # Teste com formato de texto do 'example.pdf'
    print("\n--- Teste com formato example.pdf ---")
    example_text_data = """
Relatório de Testes de QA
Status | Total
Passou | 100
Falhou | 10
Bloqueado | 5
Não Executado | 20
"""
    sample_extracted_data_example = {
        "text": example_text_data,
        "tables": [],
        "ocr_text": ""
    }
    processed_data_example = process_extracted_data(sample_extracted_data_example)
    print("--- Dados de Status Processados (example.pdf) ---")
    print(processed_data_example["df_status"])
    print("--- KPIs Calculados (example.pdf) ---")
    print(processed_data_example["kpis"])