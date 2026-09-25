import streamlit as st
from core.config import ASSET_CLASSES
from core.allocation import validate_allocation

st.header("🎯 Alocação Estratégica")

st.write("Defina percentuais-alvo por classe. O total deve ser exatamente 100%.")

targets = {}
cols = st.columns(4)
for i, cls in enumerate(ASSET_CLASSES):
    targets[cls] = cols[i % 4].number_input(
        f"{cls} (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5,
        key=f"target_{cls}",
    )

ok, total = validate_allocation(targets)
if ok:
    st.success(f"Alocação válida: {total:.2f}%")
else:
    st.error(f"A alocação totaliza {total:.2f}%. Ajuste para 100,00%.")

st.subheader("Regra sugerida para o algoritmo")
st.markdown("""
A alocação não deve ser determinada apenas pela rentabilidade passada.
O motor deverá considerar:

- necessidade de liquidez;
- horizonte;
- perfil de risco;
- taxa de retirada;
- inflação;
- concentração;
- qualidade dos ativos;
- custos;
- tributação.
""")
