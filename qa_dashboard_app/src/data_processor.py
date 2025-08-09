import pandas as pd
import numpy as np

def process_extracted_data(extracted_data):
    df_status = pd.DataFrame()
    df_tables = pd.DataFrame()
    kpis = {}
    df_grouped_by_category = pd.DataFrame()

    if extracted_data["tables"]:
        # Assumindo que a primeira tabela encontrada é a tabela de status
        status_table_data = extracted_data["tables"][0]
        if status_table_data and len(status_table_data) > 1:
            header = status_table_data[0]
            data_rows = status_table_data[1:]
            try:
                df_status = pd.DataFrame(data_rows, columns=header)
                
                # Debug: Mostrar as colunas disponíveis
                print(f"Colunas disponíveis no DataFrame: {df_status.columns.tolist()}")
                print(f"Formato do DataFrame:")
                print(df_status.head())
                
                # Tentar identificar a coluna de totais automaticamente
                total_column = identify_total_column(df_status)
                
                if total_column:
                    # Converter para numérico, tratando erros
                    df_status[total_column] = pd.to_numeric(df_status[total_column], errors='coerce')
                    df_status[total_column] = df_status[total_column].fillna(0)
                    
                    print(f"Usando a coluna '{total_column}' como coluna de totais")
                else:
                    print("Aviso: Não foi possível identificar uma coluna de totais válida")
                    
            except Exception as e:
                print(f"Erro ao criar df_status da tabela extraída: {e}")

    # Calcular KPIs com verificação robusta de colunas
    if not df_status.empty:
        kpis = calculate_kpis_robust(df_status)

    return {
        "df_status": df_status,
        "df_tables": df_tables,
        "kpis": kpis,
        "df_grouped_by_category": df_grouped_by_category
    }

def identify_total_column(df):
    """
    Tenta identificar automaticamente qual coluna contém os valores totais
    """
    # Lista de possíveis nomes para a coluna de totais
    possible_total_columns = [
        'Total', 'total', 'TOTAL',
        'Número', 'numero', 'NÚMERO', 'NUMERO',
        'Count', 'count', 'COUNT',
        'Quantidade', 'quantidade', 'QUANTIDADE',
        'Casos', 'casos', 'CASOS',
        'Total_casos', 'total_casos',
        'Qtd', 'qtd', 'QTD'
    ]
    
    # Primeiro, verificar se existe alguma coluna com nome exato
    for col_name in possible_total_columns:
        if col_name in df.columns:
            # Verificar se a coluna contém valores numéricos
            try:
                pd.to_numeric(df[col_name], errors='coerce')
                return col_name
            except:
                continue
    
    # Se não encontrou por nome, procurar por colunas com valores numéricos
    for col in df.columns:
        try:
            # Tentar converter para numérico
            numeric_values = pd.to_numeric(df[col], errors='coerce')
            # Se pelo menos 50% dos valores são numéricos e não são todos NaN
            if numeric_values.notna().sum() > len(df) * 0.5:
                return col
        except:
            continue
    
    return None

def calculate_kpis_robust(df_status):
    """
    Calcula KPIs de forma robusta, adaptando-se às colunas disponíveis
    """
    kpis = {}
    
    # Identificar colunas importantes
    total_column = identify_total_column(df_status)
    status_column = identify_status_column(df_status)
    
    if not total_column:
        print("Aviso: Não foi possível identificar coluna de totais. Usando contagem de linhas.")
        # Se não há coluna de totais, usar contagem de linhas
        total_cases = len(df_status)
        kpis["Total de Casos de Teste"] = total_cases
        kpis["Casos Passados"] = 0
        kpis["Casos Executados"] = 0
        kpis["Percentual de Execucao"] = 0
        kpis["Percentual de Sucesso"] = 0
        return kpis
    
    # Calcular totais
    total_cases = df_status[total_column].sum()
    
    if status_column:
        # Identificar status de sucesso (variações de "passou", "pass", "success", etc.)
        passed_cases = calculate_passed_cases(df_status, status_column, total_column)
        executed_cases = calculate_executed_cases(df_status, status_column, total_column)
    else:
        print("Aviso: Não foi possível identificar coluna de status")
        passed_cases = 0
        executed_cases = total_cases  # Assumir que todos foram executados se não há coluna de status
    
    # Calcular KPIs
    kpis["Total de Casos de Teste"] = int(total_cases) if not np.isnan(total_cases) else 0
    kpis["Casos Passados"] = int(passed_cases) if not np.isnan(passed_cases) else 0
    kpis["Casos Executados"] = int(executed_cases) if not np.isnan(executed_cases) else 0
    
    # Calcular percentuais
    if total_cases > 0:
        kpis["Percentual de Execucao"] = round((executed_cases / total_cases * 100), 2)
    else:
        kpis["Percentual de Execucao"] = 0
    
    if executed_cases > 0:
        kpis["Percentual de Sucesso"] = round((passed_cases / executed_cases * 100), 2)
    else:
        kpis["Percentual de Sucesso"] = 0
    
    return kpis

def identify_status_column(df):
    """
    Tenta identificar a coluna que contém o status dos testes
    """
    possible_status_columns = [
        'Status', 'status', 'STATUS',
        'Estado', 'estado', 'ESTADO',
        'Resultado', 'resultado', 'RESULTADO',
        'Result', 'result', 'RESULT'
    ]
    
    for col_name in possible_status_columns:
        if col_name in df.columns:
            return col_name
    
    # Se não encontrou por nome, procurar coluna que contém valores típicos de status
    for col in df.columns:
        if df[col].dtype == 'object':  # Coluna de texto
            unique_values = df[col].str.lower().unique() if hasattr(df[col], 'str') else []
            status_keywords = ['passou', 'falhou', 'bloqueado', 'pass', 'fail', 'blocked', 'success', 'error']
            if any(keyword in str(val).lower() for val in unique_values for keyword in status_keywords):
                return col
    
    return None

def calculate_passed_cases(df, status_column, total_column):
    """
    Calcula casos que passaram, considerando diferentes variações de texto
    """
    passed_keywords = ['passou', 'pass', 'passed', 'success', 'sucesso', 'ok']
    
    passed_mask = df[status_column].str.lower().isin(passed_keywords)
    return df[passed_mask][total_column].sum()

def calculate_executed_cases(df, status_column, total_column):
    """
    Calcula casos executados (passou + falhou + bloqueado)
    """
    executed_keywords = [
        'passou', 'pass', 'passed', 'success', 'sucesso', 'ok',
        'falhou', 'fail', 'failed', 'error', 'erro',
        'bloqueado', 'blocked', 'block'
    ]
    
    executed_mask = df[status_column].str.lower().isin(executed_keywords)
    return df[executed_mask][total_column].sum()

def debug_dataframe(df, name="DataFrame"):
    """
    Função auxiliar para debug do DataFrame
    """
    print(f"\n=== DEBUG {name} ===")
    print(f"Shape: {df.shape}")
    print(f"Colunas: {df.columns.tolist()}")
    print(f"Tipos de dados:")
    print(df.dtypes)
    print(f"Primeiras linhas:")
    print(df.head())
    print(f"Valores únicos por coluna:")
    for col in df.columns:
        unique_vals = df[col].unique()
        print(f"  {col}: {unique_vals[:5]}{'...' if len(unique_vals) > 5 else ''}")
    print("=" * 50)

if __name__ == "__main__":
    from pdf_extractor import extract_data_from_pdf
    import os

    dummy_pdf_path = "example.pdf"
    if not os.path.exists(dummy_pdf_path):
        print(f"Por favor, coloque um arquivo PDF chamado '{dummy_pdf_path}' no diretório atual para teste.")
    else:
        print(f"Extraindo dados de {dummy_pdf_path}...")
        extracted_data = extract_data_from_pdf(dummy_pdf_path)
        processed_data = process_extracted_data(extracted_data)

        print("\n--- Dados de Status Processados ---")
        debug_dataframe(processed_data["df_status"], "Status DataFrame")

        print("\n--- Dados de Tabelas Processadas (se houver) ---")
        print(processed_data["df_tables"])

        print("\n--- KPIs Calculados ---")
        for k, v in processed_data["kpis"].items():
            print(f"{k}: {v}")

        print("\n--- Dados Agrupados por Categoria (Placeholder) ---")
        print(processed_data["df_grouped_by_category"])
