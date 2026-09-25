import streamlit as st
import pandas as pd
from core.portfolio import add_asset, get_assets, delete_asset

st.header("💼 Carteira Atual")

with st.form("asset"):
    c1, c2, c3 = st.columns(3)
    ticker = c1.text_input("Ticker")
    name = c2.text_input("Nome do ativo")
    asset_class = c3.selectbox(
        "Classe",
        ["Liquidez", "Tesouro Direto", "Renda Fixa Bancária", "Ações", "FIIs", "ETFs", "Fundos", "Outros"],
    )
    c4, c5, c6 = st.columns(3)
    quantity = c4.number_input("Quantidade", min_value=0.0, value=0.0)
    unit_price = c5.number_input("Preço unitário (R$)", min_value=0.0, value=0.0)
    total_value = c6.number_input("Valor total (R$)", min_value=0.0, value=0.0, step=100.0)
    target = st.number_input("Alocação-alvo (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    action = st.selectbox("Ação", ["MANTER", "AUMENTAR", "REDUZIR", "SUBSTITUIR", "ELIMINAR"])
    notes = st.text_area("Observações")
    submitted = st.form_submit_button("Adicionar ativo")

if submitted:
    if not ticker.strip():
        st.error("Informe o ticker.")
    elif total_value <= 0:
        st.error("Informe um valor total maior que zero.")
    else:
        add_asset({
            "ticker": ticker,
            "name": name,
            "asset_class": asset_class,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_value": total_value,
            "target_percent": target,
            "action": action,
            "notes": notes,
        })
        st.success("Ativo adicionado.")

assets = get_assets()
if assets:
    df = pd.DataFrame(assets)
    st.dataframe(
        df[["id","ticker","name","asset_class","quantity","unit_price","total_value","current_percent","target_percent","action"]],
        use_container_width=True,
    )

    st.subheader("Excluir ativo")
    ids = {f"{a['ticker']} — R$ {a['total_value']:,.2f}": a["id"] for a in assets}
    selected = st.selectbox("Selecione", list(ids.keys()))
    if st.button("Excluir selecionado"):
        delete_asset(ids[selected])
        st.success("Ativo excluído. Atualize a página.")
else:
    st.info("Nenhum ativo cadastrado.")
