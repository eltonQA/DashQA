import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pdf_extractor import extract_data_from_pdf
from data_processor import process_extracted_data

def main():
    st.set_page_config(
        page_title="QA Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 QA Dashboard - Análise de Métricas de Testes")
    st.markdown("---")

    # Sidebar for file upload
    st.sidebar.header("📁 Upload de Arquivo PDF")
    uploaded_file = st.sidebar.file_uploader(
        "Selecione um arquivo PDF com métricas de QA",
        type=['pdf'],
        help="Faça upload de um arquivo PDF contendo dados de testes de QA"
    )

    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the PDF
        with st.spinner("Extraindo dados do PDF..."):
            extracted_data = extract_data_from_pdf(temp_file_path)
            processed_data = process_extracted_data(extracted_data)

        # Clean up temporary file
        os.remove(temp_file_path)

        # Display results
        if not processed_data["df_status"].empty:
            display_dashboard(processed_data)
        else:
            st.error("Não foi possível extrair dados válidos do PDF. Verifique se o arquivo contém tabelas de métricas de QA.")
    else:
        # Display sample data for demonstration
        st.info("👆 Faça upload de um arquivo PDF para visualizar as métricas de QA")
        display_sample_dashboard()

def display_dashboard(processed_data):
    df_status = processed_data["df_status"]
    kpis = processed_data["kpis"]

    # KPIs Section
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

    # Charts Section
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

    # Data Table
    st.subheader("📋 Dados Detalhados")
    st.dataframe(df_status, use_container_width=True)

    # Export functionality
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

    # Sample data
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

    # KPIs Section
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

    # Charts Section
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

    # Data Table
    st.subheader("📋 Dados de Exemplo")
    st.dataframe(sample_data, use_container_width=True)

if __name__ == "__main__":
    main()

