import streamlit as st
from core.database import init_db
from core.database import DatabaseManager

st.set_page_config(
    page_title="Planejador Financeiro — Brasil",
    page_icon="📊",
    layout="wide",
)

# Inicializa o banco de dados SQLite caso não exista
init_db()

st.title("📊 Planejador Financeiro — Brasil")
st.caption("Sistema autônomo e inteligente de gestão patrimonial, rebalanceamento e triagem de ativos.")

# Tenta carregar o resumo da carteira do banco de dados
try:
    carteira = DatabaseManager.obter_carteira()
    total_patrimonio = sum([float(a.get("valor_atual", 0.0)) for a in carteira]) if carteira else 0.0
    qtd_ativos = len(carteira)
except Exception:
    total_patrimonio = 0.0
    qtd_ativos = 0

c1, c2, c3 = st.columns(3)
c1.metric("Patrimônio Cadastrado", f"R$ {total_patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Ativos na Base", qtd_ativos)
c3.metric("Governança Macro", "Ativa (API BCB / SGS)")

st.divider()

st.subheader("🧭 Como navegar pelo sistema")
st.markdown("""
Utilize o **menu lateral esquerdo** para acessar os módulos especializados que construímos:
- **Cenário Macro & Indicadores:** Consulta em tempo real da Taxa Selic e IPCA oficial do Banco Central.
- **Simuladores & Projeções:** Simulador de Imposto de Renda Regressivo e Projeção de Independência Financeira baseada em juros reais.
- **Triagem Inteligente:** Varredura automática ou manual de FIIs, Renda Fixa, Tesouro e ETFs com base em critérios rígidos (P/VP, Vacância, FGC, Liquidez).
- **Rebalanceamento & Relatórios:** Direcionamento matemático de novos aportes e exportação executiva de dados.
""")

st.success("✨ Sistema 100% modular, determinístico e integrado pronto para uso na web!")
