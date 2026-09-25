import streamlit as st
from core.database import init_db
from core.portfolio import portfolio_summary

st.set_page_config(
    page_title="Planejador Financeiro — Brasil",
    page_icon="📊",
    layout="wide",
)

init_db()

st.title("📊 Planejador Financeiro — Brasil")
st.caption("Protótipo inicial: planejamento de aposentadoria, alocação e acompanhamento patrimonial.")

summary = portfolio_summary()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Patrimônio cadastrado", f"R$ {summary['total_value']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Ativos cadastrados", summary["asset_count"])
c3.metric("Classes", summary["class_count"])
c4.metric("Perfil", summary["profile"])

st.divider()

st.subheader("Como usar")
st.markdown("""
1. Abra **01 — Perfil** e informe idade, patrimônio, aporte e renda desejada.
2. Abra **02 — Carteira Atual** e cadastre os ativos.
3. Abra **03 — Cenário Macro** para registrar Selic, IPCA e data de referência.
4. Use **04 — Alocação** para definir os percentuais-alvo.
5. Use **05 — Projeções** para comparar cenários.
6. Use **06 — Relatório** para gerar o diagnóstico consolidado.

> O protótipo não faz recomendação automática de compra/venda e não consulta dados externos ainda.
""")

st.info("Próxima fase: integrar fontes oficiais de dados e depois adicionar uma camada opcional de IA.")
