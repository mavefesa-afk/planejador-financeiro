import streamlit as st
from core.database import DatabaseManager
from core.portfolio_integration import PortfolioIntegration
from core.macro import MacroScenario
from core.reports import ReportGenerator

st.set_page_config(page_title="Relatórios e Exportação - Planejador Financeiro", page_icon="📄", layout="wide")

st.title("📄 Central de Relatórios e Exportação Executiva")
st.markdown("Exporte os dados consolidados da sua carteira, diagnósticos e métricas em formatos compatíveis com planilhas e arquivos executivos.")

carteira = DatabaseManager.obter_carteira()
macro = MacroScenario()
ipca_atual = macro.get_indicator("ipca_12m")["valor"]

if not carteira:
    st.warning("⚠️ Nenhum ativo cadastrado no banco de dados para gerar relatórios.")
else:
    diagnostico = PortfolioIntegration.analisar_carteira(carteira, ipca_atual)
    
    st.subheader("📊 Prévia do Relatório Consolidado")
    col1, col2 = st.columns(2)
    col1.metric("Total de Ativos", diagnostico["total_analisados"])
    col2.metric("Ativos Aprovados", diagnostico["aprovados"])

    st.markdown("---")
    st.subheader("📥 Opções de Download")

    col_down1, col_down2 = st.columns(2)

    with col_down1:
        st.markdown("**Exportar Ativos em CSV (Planilhas)**")
        df_ativos = ReportGenerator.gerar_dataframe_ativos(carteira)
        csv_data = df_ativos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dados da Carteira (CSV)",
            data=csv_data,
            file_name="carteira_planejador.csv",
            mime="text/csv"
        )

    with col_down2:
        st.markdown("**Exportar Relatório Executivo Completo (JSON)**")
        json_str = ReportGenerator.gerar_json_executivo(carteira, diagnostico)
        st.download_button(
            label="📥 Baixar Relatório Completo (JSON)",
            data=json_str,
            file_name="relatorio_executivo_financeiro.json",
            mime="application/json"
        )
