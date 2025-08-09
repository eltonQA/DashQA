import pandas as pd

def process_extracted_data(extracted_data):
    df_status = pd.DataFrame()
    df_tables = pd.DataFrame()
    kpis = {}
    df_grouped_by_category = pd.DataFrame()

    if extracted_data["tables"]:
        # Assumindo que a primeira tabela encontrada é a tabela de status
        # Isso precisa ser mais robusto para PDFs do mundo real
        status_table_data = extracted_data["tables"][0]
        if status_table_data and len(status_table_data) > 1:
            header = status_table_data[0]
            data_rows = status_table_data[1:]
            try:
                df_status = pd.DataFrame(data_rows, columns=header)
                
                # Verifica se a coluna 'Total' existe antes de tentar convertê-la
                if "Total" in df_status.columns:
                    df_status["Total"] = pd.to_numeric(df_status["Total"], errors='coerce').fillna(0)
                else:
                    # Se a coluna não for encontrada, imprime um aviso e define o DataFrame como vazio para evitar erros
                    print("Aviso: Coluna 'Total' não encontrada no DataFrame de status.")
                    df_status = pd.DataFrame()

            except Exception as e:
                print(f"Erro ao criar df_status a partir da tabela extraída: {e}")

    if not df_status.empty:
        total_cases = df_status["Total"].sum()
        passed_cases = df_status[df_status["Status"] == "Passou"]["Total"].sum()
        executed_cases = df_status[df_status["Status"].isin(["Passou", "Falhou", "Bloqueado"])]["Total"].sum()

        kpis["Total de Casos de Teste"] = total_cases
        kpis["Casos Passados"] = passed_cases
        kpis["Casos Executados"] = executed_cases
        kpis["Percentual de Execucao"] = (executed_cases / total_cases * 100) if total_cases > 0 else 0
        kpis["Percentual de Sucesso"] = (passed_cases / executed_cases * 100) if executed_cases > 0 else 0
    else:
        # Define os KPIs como zero se o DataFrame estiver vazio
        kpis["Total de Casos de Teste"] = 0
        kpis["Casos Passados"] = 0
        kpis["Casos Executados"] = 0
        kpis["Percentual de Execucao"] = 0
        kpis["Percentual de Sucesso"] = 0

    return {
        "df_status": df_status,
        "df_tables": df_tables,
        "kpis": kpis,
        "df_grouped_by_category": df_grouped_by_category
    }

if __name__ == "__main__":
    from pdf_extractor import extract_data_from_pdf
    import os

    dummy_pdf_path = "example.pdf"
    if not os.path.exists(dummy_pdf_path):
        print(f"Por favor, coloque um arquivo PDF chamado '{dummy_pdf_path}' no diretório atual para testes.")
    else:
        print(f"Extraindo dados de {dummy_pdf_path}...")
        extracted_data = extract_data_from_pdf(dummy_pdf_path)
        processed_data = process_extracted_data(extracted_data)

        print("\n--- Processed Status Data ---")
        print(processed_data["df_status"])

        print("\n--- Processed Tables Data (if any) ---")
        print(processed_data["df_tables"])

        print("\n--- Calculated KPIs ---")
        for k, v in processed_data["kpis"].items():
            print(f"{k}: {v}")

        print("\n--- Grouped by Category Data (Placeholder) ---")
        print(processed_data["df_grouped_by_category"])
