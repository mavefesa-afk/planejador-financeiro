import streamlit as st
from core.macro import MacroScenario
from core.database import DatabaseManager
from core.portfolio_integration import PortfolioIntegration

st.set_page_config(page_title="Diagnóstico da Carteira - Planejador Financeiro", page_icon="📊", layout="wide")

st.title("📊 Diagnóstico Inteligente da Carteira")
st.markdown("Cruzamento automático dos ativos cadastrados na sua carteira (via SQLite) com os critérios rigorosos de qualidade, segurança e rentabilidade real.")

# Carrega cenário macro
macro = MacroScenario()
ipca_atual = macro.get_indicator("ipca_12m")["valor"]

st.sidebar.header("Cenário Macro de Referência")
st.sidebar.metric("IPCA (12m)", f"{ipca_atual * 100:.2f}% a.a.")

# Busca os ativos reais cadastrados no banco de dados SQLite
carteira_db = DatabaseManager.obter_carteira()

if not carteira_db:
    st.warning("⚠️ Nenhum ativo encontrado no banco de dados da carteira.")
    st.info("💡 Vá até a página **Cadastrar Ativo** no menu lateral para adicionar seus investimentos (FIIs, Ações, Renda Fixa) e realizar o diagnóstico.")
else:
    # Executa o diagnóstico com os dados reais do SQLite
    diagnostico = PortfolioIntegration.analisar_carteira(carteira_db, ipca_atual)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ativos na Carteira", diagnostico["total_analisados"])
    col2.metric("Ativos Aprovados na Estratégia", diagnostico["aprovados"])
    col3.metric("Ativos com Alertas / Fora do Perfil", diagnostico["reprovados"])

    st.markdown("---")
    st.subheader("Detalhamento e Validação por Ativo")

    for item in diagnostico["detalhes"]:
        with st.expander(f"{'✅' if item.get('aprovado') else '⚠️'} [{item['classe']}] {item.get('ativo', 'Ativo')}"):
            if item.get("aprovado"):
                st.success("Ativo em conformidade total com as regras estabelecidas.")
                if "dy_real" in item:
                    st.write(f"- **DY Real Calculado:** {item['dy_real'] * 100:.2f}% a.a.")
            else:
                st.error("Ativo apresenta desvios em relação à estratégia planejada.")
                st.markdown("**Pontos de atenção identificados:**")
                for motivo in item.get("motivos", []):
                    st.write(f"- {motivo}")
