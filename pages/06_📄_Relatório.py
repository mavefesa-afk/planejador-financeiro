import streamlit as st
from core.profile import get_profile
from core.portfolio import get_assets
from core.database import get_connection
from core.report import portfolio_text

st.header("📄 Relatório Consolidado")

profile = get_profile()
assets = get_assets()

conn = get_connection()
row = conn.execute("SELECT * FROM macro_snapshot ORDER BY reference_date DESC, id DESC LIMIT 1").fetchone()
conn.close()
macro = dict(row) if row else None

st.subheader("Resumo")
st.text(portfolio_text(profile, assets, macro))

st.subheader("Carteira")
if assets:
    import pandas as pd
    st.dataframe(pd.DataFrame(assets), use_container_width=True)
else:
    st.info("Nenhum ativo cadastrado.")

st.subheader("Próxima evolução")
st.markdown("""
O relatório definitivo deverá incorporar:

- dados de mercado atualizados;
- análise dos FIIs;
- análise dos ETFs;
- tributação por ativo;
- controle de FGC;
- concentração por emissor/setor;
- recomendação de rebalanceamento;
- simulação de sustentabilidade da retirada;
- exportação em PDF/Excel;
- histórico das análises.
""")
