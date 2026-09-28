import streamlit as st
from core.calculations import FinancialCalculations

st.set_page_config(page_title="Simulador de IR Regressivo - Planejador Financeiro", page_icon="💸", layout="wide")

st.title("💸 Simulador de Imposto de Renda Regressivo (Renda Fixa)")
st.markdown("Calcule o impacto exato da tabela regressiva do IR (de 22.5% a 15%) sobre o rendimento de aplicações em Renda Fixa.")

with st.form("form_simulador_ir"):
    col1, col2 = st.columns(2)
    
    with col1:
        valor_aplicado = st.number_input("Valor Aplicado (Principal) (R$)", value=10000.0, step=1000.0)
        valor_bruto = st.number_input("Valor Bruto Final (Resgate) (R$)", value=13000.0, step=500.0)
    
    with col2:
        dias_investido = st.number_input("Prazo do Investimento (em dias)", value=500, step=30)

    submitted = st.form_submit_button("Calculador Rentabilidade Líquida")
    
    if submitted:
        resultado = FinancialCalculations.calcular_rendimento_liquido(valor_aplicado, valor_bruto, int(dias_investido))
        aliquota_percentual = resultado["aliquota_ir"] * 100
        
        st.markdown("---")
        st.subheader("📊 Resultados da Simulação")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Lucro Bruto", f"R$ {resultado['lucro_bruto']:,.2f}")
        col_res2.metric("Alíquota de IR Aplicada", f"{aliquota_percentual:.1f}%", help="Baseado no prazo em dias informado.")
        col_res3.metric("Imposto Devido (IR)", f"R$ {resultado['imposto_devido']:,.2f}", delta_color="inverse")
        
        st.markdown("---")
        col_res4, col_res5 = st.columns(2)
        col_res4.metric("Valor Líquido do Resgate", f"R$ {resultado['valor_liquido']:,.2f}")
        col_res5.metric("Lucro Líquido (Após IR)", f"R$ {resultado['lucro_liquido']:,.2f}")

        # Explicação da faixa
        st.info(f"ℹ️ Prazo de **{dias_investido} dias** enquadra-se na faixa de tributação de **{aliquota_percentual:.1f}%** sobre o rendimento.")
