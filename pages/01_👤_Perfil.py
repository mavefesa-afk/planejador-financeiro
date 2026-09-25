import streamlit as st
from core.profile import save_profile, get_profile
from core.calculations import withdrawal_rate

st.header("👤 Perfil e Objetivos")

p = get_profile() or {}

with st.form("profile"):
    age = st.number_input("Idade", 18, 110, int(p.get("age") or 65))
    horizon = st.number_input("Horizonte (anos)", 1, 60, int(p.get("horizon_years") or 15))
    situation = st.selectbox(
        "Situação",
        ["Acumulação", "Pré-aposentadoria", "Aposentadoria", "Distribuição"],
        index=["Acumulação", "Pré-aposentadoria", "Aposentadoria", "Distribuição"].index(
            p.get("situation") or "Aposentadoria"
        ),
    )
    patrimony = st.number_input("Patrimônio atual (R$)", min_value=0.0, value=float(p.get("initial_patrimony") or 350000), step=1000.0)
    contribution = st.number_input("Aporte mensal (R$)", min_value=0.0, value=float(p.get("monthly_contribution") or 0), step=100.0)
    desired = st.number_input("Renda mensal desejada (R$)", min_value=0.0, value=float(p.get("desired_monthly_income") or 2000), step=100.0)
    minimum = st.number_input("Renda mensal mínima (R$)", min_value=0.0, value=float(p.get("minimum_monthly_income") or desired), step=100.0)
    other_income = st.number_input("Outras rendas mensais (R$)", min_value=0.0, value=float(p.get("other_monthly_income") or 0), step=100.0)
    risk = st.selectbox("Perfil de risco", ["Conservador", "Moderado", "Arrojado", "Agressivo"], index=["Conservador","Moderado","Arrojado","Agressivo"].index(p.get("risk_profile") or "Moderado"))
    liquidity = st.number_input("Reserva desejada (meses)", 1.0, 36.0, float(p.get("liquidity_months") or 12.0), step=1.0)
    notes = st.text_area("Observações", value=p.get("notes") or "")
    submitted = st.form_submit_button("Salvar perfil")

if submitted:
    save_profile({
        "age": age,
        "horizon_years": horizon,
        "situation": situation,
        "initial_patrimony": patrimony,
        "monthly_contribution": contribution,
        "desired_monthly_income": desired,
        "minimum_monthly_income": minimum,
        "risk_profile": risk,
        "liquidity_months": liquidity,
        "other_monthly_income": other_income,
        "notes": notes,
    })
    st.success("Perfil salvo.")

st.divider()

if patrimony > 0:
    rate = withdrawal_rate(desired, patrimony)
    st.metric("Taxa de retirada anual", f"{rate:.2%}")
    if rate > 0.08:
        st.warning("Taxa de retirada elevada para um patrimônio que também precisa crescer. Avalie a sustentabilidade nos cenários.")
