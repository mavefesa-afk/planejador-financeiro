import streamlit as st
import pandas as pd
from core.profile import get_profile
from core.calculations import future_value, future_real_value, withdrawal_rate
from core.config import DEFAULT_RETURN_SCENARIOS, DEFAULT_INFLATION

st.header("📈 Projeções")

profile = get_profile()

if not profile:
    st.warning("Cadastre primeiro o perfil na página 01 — Perfil.")
    st.stop()

inflation = st.number_input("Inflação anual (%)", min_value=-20.0, max_value=100.0, value=DEFAULT_INFLATION*100, step=0.1) / 100

rows = []
for name, ret in DEFAULT_RETURN_SCENARIOS.items():
    fv10 = future_value(profile["initial_patrimony"], profile["monthly_contribution"], ret, 10)
    real10 = future_real_value(fv10, inflation, 10)
    fv_h = future_value(profile["initial_patrimony"], profile["monthly_contribution"], ret, profile["horizon_years"])
    real_h = future_real_value(fv_h, inflation, profile["horizon_years"])
    rows.append({
        "Cenário": name,
        "Retorno anual": ret,
        "Patrimônio em 10 anos": fv10,
        "Patrimônio real em 10 anos": real10,
        f"Patrimônio em {profile['horizon_years']} anos": fv_h,
        f"Patrimônio real em {profile['horizon_years']} anos": real_h,
    })

df = pd.DataFrame(rows)
for col in ["Retorno anual"]:
    df[col] = df[col].map(lambda x: f"{x:.2%}")

st.dataframe(
    df.style.format({
        "Patrimônio em 10 anos": "R$ {:,.2f}",
        "Patrimônio real em 10 anos": "R$ {:,.2f}",
        f"Patrimônio em {profile['horizon_years']} anos": "R$ {:,.2f}",
        f"Patrimônio real em {profile['horizon_years']} anos": "R$ {:,.2f}",
    }),
    use_container_width=True,
)

rate = withdrawal_rate(profile["desired_monthly_income"], profile["initial_patrimony"])
st.metric("Taxa de retirada anual atual", f"{rate:.2%}")
