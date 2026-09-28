import streamlit as st
from core.macro import MacroScenario
from core.projections import FinancialProjections

st.set_page_config(page_title="Projeção de Independência - Planejador Financeiro", page_icon="📈", layout="wide")

st.title("📈 Projeção de Independência Financeira")
st.markdown("Simule sua jornada rumo à liberdade financeira considerando o crescimento real do patrimônio (juros descontados da inflação).")

# Carrega cenário macro para sugerir o juro real atual
macro = MacroScenario()
juro_real_padrao = macro.calcular_juro_real()

with st.form("form_projecao"):
    col1, col2 = st.columns(2)
    
    with col1:
        patrimonio_atual = st.number_input("Patrimônio Atual Acumulado (R$)", value=50000.0, step=5000.0)
        aporte_mensal = st.number_input("Aporte Mensal Previsto (R$)", value=2000.0, step=200.0)
    
    with col2:
        renda_desejada = st.number_input("Renda Passiva Mensal Desejada (Valores de Hoje) (R$)", value=10000.0, step=500.0)
        juro_real_anual = st.number_input(
            "Taxa de Juro Real Esperada (% a.a. acima da inflação)", 
            value=float(juro_real_padrao * 100), 
            step=0.5
        ) / 100.0

    submitted = st.form_submit_button("🚀 Calcular Projeção")

if submitted:
    resultado = FinancialProjections.projetar_independencia(
        patrimonio_atual=patrimonio_atual,
        aporte_mensal=aporte_mensal,
        juro_real_anual=juro_real_anual,
        renda_passiva_desejada_mensal=renda_desejada
    )

    st.markdown("---")
    st.subheader("🎯 Metas e Resultados da Projeção")

    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("Patrimônio Alvo Necessário", f"R$ {resultado['patrimonio_alvo']:,.2f}", help="Montante necessário para gerar a renda desejada apenas com o rendimento real.")
    
    if resultado["alcancavel"]:
        col_res2.metric("Tempo para Independência", f"{resultado['anos']} anos e {resultado['meses_restantes']} meses")
    else:
        col_res2.metric("Tempo para Independência", "Mais de 100 anos")
        
    col_res3.metric("Juro Real Utilizado", f"{juro_real_anual * 100:.2f}% a.a.")

    if resultado["alcancavel"]:
        st.success(f"🎉 Mantendo este ritmo, você alcançará a sua independência financeira em **{resultado['anos']} anos**!")
        
        # Gráfico de evolução patrimonial
        if resultado["trajetoria"]:
            st.subheader("Evolução do Patrimônio ao Longo dos Anos (Valores Reais)")
            dados_chart = {item["ano"]: item["patrimonio"] for item in resultado["trajetoria"]}
            st.line_chart(dados_chart)
    else:
        st.warning("⚠️ Os parâmetros atuais (aporte vs. renda desejada) indicam que o patrimônio alvo é muito distante. Tente aumentar o aporte mensal ou revisar a meta de renda.")
