import streamlit as st
from core.macro import MacroScenario
from core.filters import AssetFilters
from core.portfolio_integration import PortfolioIntegration

st.set_page_config(page_title="Diagnóstico da Carteira - Planejador Financeiro", page_icon="📊", layout="wide")

st.title("📊 Diagnóstico Inteligente da Carteira")
st.markdown("Cruzamento automático dos ativos da sua carteira atual com os critérios rigorosos de qualidade, segurança e rentabilidade real.")

# Carrega cenário macro
macro = MacroScenario()
ipca_atual = macro.get_indicator("ipca_12m")["valor"]

st.info(f"ℹ️ Os filtros estão utilizando o IPCA acumulado de referência de **{ipca_atual * 100:.2f}% a.a.** para o cálculo do DY Real.")

# Simulação de exemplo de carteira atual do usuário (pode ser conectado ao SQLite futuramente)
st.subheader("Simulação de Ativos na Carteira Atual")
st.markdown("Abaixo estão alguns exemplos de ativos cadastrados na carteira para teste do diagnóstico:")

# Exemplo interativo ou pré-carregado de ativos da carteira
carteira_exemplo = [
    {"ticker": "HGLG11", "classe": "FII", "tipo": "tijolo", "liquidez_diaria": 1500000.0, "p_vp": 0.96, "vacancia": 0.03, "dy_nominal_12m": 0.10},
    {"ticker": "MXRF11", "classe": "FII", "tipo": "papel", "liquidez_diaria": 4000000.0, "p_vp": 1.02, "vacancia": 0.0, "dy_nominal_12m": 0.12},
    {"ticker": "TAEE11", "classe": "AÇÃO", "setor": "Energia Elétrica", "historico_dividendos_consistente": True},
    {"nome": "CDB Banco XYZ (Sem FGC)", "classe": "RENDA FIXA", "tipo": "cdb", "indexador": "CDI", "cobertura_fgc": False}
]

# Executa o diagnóstico
diagnostico = PortfolioIntegration.analisar_carteira(carteira_exemplo, ipca_atual)

col1, col2, col3 = st.columns(3)
col1.metric("Total de Ativos Analisados", diagnostico["total_analisados"])
col2.metric("Ativos Aprovados na Estratégia", diagnostico["aprovados"], delta_color="normal")
col3.metric("Ativos com Alertas / Fora do Perfil", diagnostico["reprovados"], delta_color="inverse")

st.markdown("---")
st.subheader("Detalhamento por Ativo")

for item in diagnostico["detalhes"]:
    with st.expander(f"{'✅' if item.get('aprovado') else '⚠️'} [{item['classe']}] {item.get('ativo', 'Ativo')}"):
        if item.get("aprovado"):
            st.success("Ativo em conformidade total com as regras estabelecidas.")
            if "dy_real" in item:
                st.write(f"- **DY Real Calculado:** {item['dy_real'] * 100:.2f}% a.a.")
        else:
            st.error("Ativo apresenta desvios em relação à estratégia planejada.")
            st.markdown("**Pontos de atenção:**")
            for motivo in item.get("motivos", []):
                st.write(f"- {motivo}")
