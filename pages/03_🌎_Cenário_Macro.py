import streamlit as st
from datetime import date
from core.database import get_connection

st.header("🌎 Cenário Macroeconômico")

with st.form("macro"):
    ref_date = st.date_input("Data de referência", value=date.today())
    c1, c2, c3 = st.columns(3)
    selic = c1.number_input("Selic (% a.a.)", min_value=0.0, value=13.75, step=0.25)
    ipca = c2.number_input("IPCA 12 meses (%)", min_value=-20.0, max_value=100.0, value=4.22, step=0.01)
    ipca_ytd = c3.number_input("IPCA acumulado no ano (%)", min_value=-20.0, max_value=100.0, value=0.0, step=0.01)
    c4, c5 = st.columns(2)
    infl_exp = c4.number_input("Expectativa de inflação (%)", min_value=-20.0, max_value=100.0, value=4.0, step=0.01)
    selic_exp = c5.number_input("Expectativa Selic (%)", min_value=0.0, value=13.0, step=0.25)
    source = st.text_input("Fonte")
    notes = st.text_area("Observações")
    submitted = st.form_submit_button("Salvar snapshot")

if submitted:
    conn = get_connection()
    conn.execute("""
        INSERT INTO macro_snapshot
        (reference_date, selic, ipca_12m, ipca_ytd, inflation_expectation, selic_expectation, source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ref_date.isoformat(), selic/100, ipca/100, ipca_ytd/100, infl_exp/100, selic_exp/100, source, notes))
    conn.commit()
    conn.close()
    st.success("Cenário salvo.")

conn = get_connection()
rows = conn.execute("SELECT * FROM macro_snapshot ORDER BY reference_date DESC, id DESC").fetchall()
conn.close()

if rows:
    import pandas as pd
    df = pd.DataFrame([dict(r) for r in rows])
    for col in ["selic","ipca_12m","ipca_ytd","inflation_expectation","selic_expectation"]:
        df[col] = df[col] * 100
    st.dataframe(df, use_container_width=True)
