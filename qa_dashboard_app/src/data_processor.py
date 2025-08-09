import pandas as pd

def process_extracted_data(extracted_data):
    df_status = pd.DataFrame()
    kpis = {}
    grouped_data = pd.DataFrame()

    tables = extracted_data["tables"]
    text_data = extracted_data["text"]

    status_keywords = ["Passou", "Falhado", "Bloqueado", "Não Executado"]
    status_counts = {keyword: 0 for keyword in status_keywords}

    # Try to find status data from tables first
    for table in tables:
        for row in table:
            for cell in row:
                if cell:
                    for keyword in status_keywords:
                        if keyword.lower() in cell.lower():
                            status_counts[keyword] += 1

    # Convert status_counts to a DataFrame
    if any(status_counts.values()):
        df_status = pd.DataFrame(list(status_counts.items()), columns=["Status", "Total"])
        df_status = df_status[df_status["Total"] > 0] # Only include statuses that were found
    else:
        # Fallback to previous text-based extraction if no tables found or relevant columns are missing
        # This part is for the \'example.pdf\' format
        lines = text_data.split("\n")
        status_data = []
        table_header_found = False
        for line in lines:
            line = line.strip()
            if "Status | Total" in line:
                table_header_found = True
                continue
            if table_header_found and line:
                parts = line.split("|")
                if len(parts) == 2:
                    status = parts[0].strip()
                    try:
                        total = int(parts[1].strip())
                        status_data.append([status, total])
                    except ValueError:
                        pass # Ignore lines where Total is not a number
        if status_data:
            df_status = pd.DataFrame(status_data, columns=["Status", "Total"])

    # Calculate KPIs
    if not df_status.empty:
        total_cases = df_status["Total"].sum()
        passed_cases = df_status[df_status["Status"].str.contains("Passou", case=False)]["Total"].sum()
        executed_cases = df_status[~df_status["Status"].str.contains("Não Executado", case=False)]["Total"].sum()

        percent_execution = (executed_cases / total_cases) * 100 if total_cases > 0 else 0
        percent_success = (passed_cases / executed_cases) * 100 if executed_cases > 0 else 0

        kpis = {
            "Total de Casos de Teste": total_cases,
            "Casos Passados": passed_cases,
            "Casos Executados": executed_cases,
            "Percentual de Execucao": percent_execution,
            "Percentual de Sucesso": percent_success
        }

    return {
        "df_status": df_status,
        "kpis": kpis,
        "grouped_data": grouped_data # Placeholder for now
    }

if __name__ == "__main__":
    # This part is for testing the data_processor independently
    # You would typically call process_extracted_data from dashboard.py
    # For a quick test, let\'s simulate some extracted data
    sample_extracted_data = {
        "text": "",
        "tables": [
            # Sample table structure from TestLink1.9.20[fixed].pdf
            [
                ["#:", "Ações do Passo:", "Resultados Esperados::", "Estado da\nExecução:"],
                ["1", "Dado que o usuário sincroniza os pedidos\nQuando o usuário entra na tela de “Meus\npedidos”", "Então o banner aparece conforme\nfigma.", "Passou"]
            ],
            # Another sample table with \'Resultado da Execução:\'
            [
                ["Build", "SP49_C1", None, None],
                ["Testador", "mateus.sandes", None, None],
                ["Resultado da Execução:", "Falhado", None, None],
                ["Modo de Execução:", "Manual", None, None]
            ]
        ],
        "ocr_text": ""
    }

    processed_data = process_extracted_data(sample_extracted_data)
    print("--- Processed Status Data ---")
    print(processed_data["df_status"])
    print("--- Calculated KPIs ---")
    print(processed_data["kpis"])

    # Test with the original example.pdf format
    print("\n--- Testing with example.pdf format ---")
    example_text_data = """
Relatorio de Testes de QA
Status | Total
Passou | 100
Falhou | 10
Bloqueado | 5
Nao Executado | 20
"""
    sample_extracted_data_example = {
        "text": example_text_data,
        "tables": [],
        "ocr_text": ""
    }
    processed_data_example = process_extracted_data(sample_extracted_data_example)
    print("--- Processed Status Data (example.pdf) ---")
    print(processed_data_example["df_status"])
    print("--- Calculated KPIs (example.pdf) ---")
    print(processed_data_example["kpis"])


