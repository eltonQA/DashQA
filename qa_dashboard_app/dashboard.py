import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys

# Importa a biblioteca de IA da Google para usar os modelos Gemini
import google.generativeai as genai

# Adiciona o diretório src ao path para importar nossos módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_extractor import extract_data_from_pdf
from data_processor import process_extracted_data

# --- Configuração da API de IA ---
# Para usar a API, você precisa de uma chave.
# Obtenha sua chave em https://aistudio.google.com/app/apikey e substitua o texto abaixo.
# Para este exemplo, a chave é definida diretamente no código.
# Em produção, a recomendação é usar st.secrets.

# 💡 ATUALIZE o valor abaixo com a sua chave da API do Google Gemini.
GOOGLE_API_KEY = "AIzaSyBn-1G3GFapqouuvG_DV4"

# Configura a API de IA
if GOOGLE_API_KEY and GOOGLE_API_KEY != "SUA_CHAVE_AQUI":
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.warning("A chave da API da Google não foi configurada. A função de IA não estará disponível.")
    genai = None # Garante que genai seja None se a chave não for válida


# Função para gerar o texto com IA
def generate_ai_text(df_status, kpis):
    if not genai:
        return "Erro: A chave da API de IA não foi configurada."

    try:
        # Usa o modelo gemini-1.5-flash, que é um modelo de uso gratuito
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepara o prompt com base nos dados e KPIs
        prompt = f"""
        Com base nos seguintes dados de um dashboard de métricas de QA (Quality Assurance),
        crie um resumo profissional, claro e conciso para ser publicado no Teams.
        O resumo deve usar **emojis relevantes** 📊, e formatar **palavras-chave** importantes em **negrito**.
        O texto deve destacar os pontos principais, como o total de casos, o percentual de sucesso,
        e a distribuição dos status de teste. O resumo deve ser direto e de fácil leitura.

        ### Dados do Dashboard:
        - KPIs:
            - Total de Casos de Teste: {kpis.get("Total de Casos de Teste", 0)}
            - Casos Passados: {kpis.get("Casos Passados", 0)}
            - Percentual de Execução: {kpis.get("Percentual de Execucao", 0):.1f}%
            - Percentual de Sucesso: {kpis.get("Percentual de Sucesso", 0):.1f}%

        - Distribuição por Status:
        """
        for index, row in df_status.iterrows():
            prompt += f"    - {row['Status']}: {row['Total']} casos\n"

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar texto: {e}"

def main():
    st.set_page_config(
        page_title="QA Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 QA Dashboard - Análise de Métricas de Testes")
    st.markdown("---")

    # Sidebar para upload de arquivo
    st.sidebar.header("📁 Upload de Arquivo PDF")
    uploaded_file = st.sidebar.file_uploader(
        "Selecione um arquivo PDF com métricas de QA",
        type=['pdf'],
        help="Faça upload de um arquivo PDF contendo dados de testes de QA"
    )

    if uploaded_file is not None:
        # Salva o arquivo temporariamente
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Processa o PDF
        with st.spinner("Extraindo dados do PDF..."):
            extracted_data = extract_data_from_pdf(temp_file_path)
            processed_data = process_extracted_data(extracted_data)

        # Limpa o arquivo temporário
        os.remove(temp_file_path)

        # Exibe os resultados
        if not processed_data["df_status"].empty:
            display_dashboard(processed_data)
            
            # --- Seção de Geração de Texto com IA ---
            st.markdown("---")
            st.header("🤖 Gerar Resumo para Teams com IA")
            
            ai_text_placeholder = st.empty()
            
            if st.button("✨ Gerar Resumo"):
                with st.spinner("Gerando texto com IA..."):
                    ai_text = generate_ai_text(
                        processed_data["df_status"],
                        processed_data["kpis"]
                    )
                    ai_text_placeholder.text_area(
                        "Texto gerado:", 
                        ai_text, 
                        height=200
                    )
        else:
            st.error("Não foi possível extrair dados válidos do PDF. Verifique se o arquivo contém tabelas de métricas de QA.")
    else:
        # Exibe dados de exemplo para demonstração
        st.info("👆 Faça upload de um arquivo PDF para visualizar as métricas de QA")
        display_sample_dashboard()

def display_dashboard(processed_data):
    df_status = processed_data["df_status"]
    kpis = processed_data["kpis"]

    # Seção de KPIs
    st.header("📈 KPIs Principais")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total de Casos de Teste",
            value=kpis.get("Total de Casos de Teste", 0)
        )

    with col2:
        st.metric(
            label="Casos Passados",
            value=kpis.get("Casos Passados", 0)
        )

    with col3:
        st.metric(
            label="Percentual de Execução",
            value=f"{kpis.get('Percentual de Execucao', 0):.1f}%"
        )

    with col4:
        st.metric(
            label="Percentual de Sucesso",
            value=f"{kpis.get('Percentual de Sucesso', 0):.1f}%"
        )

    st.markdown("---")

    # Seção de gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribuição por Status")
        fig_pie = px.pie(
            df_status,
            values='Total',
            names='Status',
            title="Total de Casos por Status",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📈 Casos por Status")
        fig_bar = px.bar(
            df_status,
            x='Status',
            y='Total',
            title="Número de Casos por Status",
            color='Status',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Tabela de dados
    st.subheader("📋 Dados Detalhados")
    st.dataframe(df_status, use_container_width=True)

    # Funcionalidade de exportação
    st.subheader("💾 Exportar Dados")
    csv = df_status.to_csv(index=False)
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="qa_metrics.csv",
        mime="text/csv"
    )

def display_sample_dashboard():
    st.header("📊 Dashboard de Exemplo")
    st.info("Este é um exemplo de como o dashboard aparecerá com dados reais.")

    # Dados de exemplo
    sample_data = pd.DataFrame({
        'Status': ['Passou', 'Falhou', 'Bloqueado', 'Não Executado'],
        'Total': [100, 10, 5, 20]
    })

    sample_kpis = {
        "Total de Casos de Teste": 135,
        "Casos Passados": 100,
        "Percentual de Execucao": 85.2,
        "Percentual de Sucesso": 87.0
    }

    # Seção de KPIs
    st.subheader("📈 KPIs Principais")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total de Casos de Teste",
            value=sample_kpis["Total de Casos de Teste"]
        )

    with col2:
        st.metric(
            label="Casos Passados",
            value=sample_kpis["Casos Passados"]
        )

    with col3:
        st.metric(
            label="Percentual de Execução",
            value=f"{sample_kpis['Percentual de Execucao']:.1f}%"
        )

    with col4:
        st.metric(
            label="Percentual de Sucesso",
            value=f"{sample_kpis['Percentual de Sucesso']:.1f}%"
        )

    # Seção de gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribuição por Status")
        fig_pie = px.pie(
            sample_data,
            values='Total',
            names='Status',
            title="Total de Casos por Status",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📈 Casos por Status")
        fig_bar = px.bar(
            sample_data,
            x='Status',
            y='Total',
            title="Número de Casos por Status",
            color='Status',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Tabela de dados
    st.subheader("📋 Dados de Exemplo")
    st.dataframe(sample_data, use_container_width=True)

if __name__ == "__main__":
    main()