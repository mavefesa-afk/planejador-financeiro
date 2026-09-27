import streamlit as st
from core.macro import MacroScenario
from core.filters import AssetFilters

st.set_page_config(page_title="Filtros de Ativos - Planejador Financeiro", page_icon="🔍", layout="wide")

st.title("🔍 Análise e Seleção de Ativos")
st.markdown("Filtre e valide ativos (FIIs, Ações e Renda Fixa) com base nos critérios rigorosos definidos no seu planejamento.")

# Instancia o cenário macro e os filtros
macro = MacroScenario()
ipca_atual = macro.get_indicator("ipca_12m")["valor"]
selic_atual = macro.get_indicator("selic_anual")["valor"]

st.sidebar.header("Cenário Macro de Referência")
st.sidebar.metric("Selic Atual", f"{selic_atual * 100:.2f}% a.a.")
st.sidebar.metric("IPCA (12m)", f"{ipca_atual * 100:.2f}% a.a.")

juro_real = macro.calcular_juro_real()
st.sidebar.metric("Juro Real (Selic / IPCA)", f"{juro_real * 100:.2f}% a.a.")

tab1, tab2, tab3 = st.tabs(["🏢 Fundos Imobiliários (FIIs)", "📈 Ações", "💰 Renda Fixa & Tesouro"])

with tab1:
    st.subheader("Simulador de Filtro para FIIs")
    col1, col2 = st.columns(2)
    
    with col1:
        ticker_fii = st.text_input("Ticker do FII", value="HGLG11")
        tipo_fii = st.selectbox("Tipo de FII", options=["tijolo", "papel", "híbrido"])
        liquidez_fii = st.number_input("Liquidez Média Diária (R$)", value=1200000.0, step=50000.0)
    
    with col2:
        p_vp_fii = st.number_input("P/VP", value=0.95, step=0.01)
        vacancia_fii = st.slider("Taxa de Vacância (%)", min_value=0.0, max_value=30.0, value=3.0) / 100.0
        dy_nominal_fii = st.slider("DY Nominal (12m) (%)", min_value=0.0, max_value=20.0, value=10.5) / 100.0

    if st.button("Analisar FII"):
        fii_data = {
            "ticker": ticker_fii.upper(),
            "tipo": tipo_fii,
            "liquidez_diaria": liquidez_fii,
            "p_vp": p_vp_fii,
            "vacancia": vacancia_fii,
            "dy_nominal_12m": dy_nominal_fii
        }
        resultado = AssetFilters.filtrar_fiis(fii_data, ipca_atual)
        
        if resultado["aprovado"]:
            st.success(f"✅ O FII **{resultado['ativo']}** foi **APROVADO** pelos critérios!")
            st.info(f"DY Real Calculado: **{resultado['dy_real'] * 100:.2f}% a.a.**")
        else:
            st.error(f"❌ O FII **{resultado['ativo']}** foi **REPROVADO**.")
            st.warning(f"DY Real Calculado: {resultado['dy_real'] * 100:.2f}% a.a.")
            st.markdown("**Motivos da reprovação:**")
            for motivo in resultado["motivos"]:
                st.write(f"- {motivo}")

with tab2:
    st.subheader("Simulador de Filtro para Ações")
    col1, col2 = st.columns(2)
    with col1:
        ticker_acao = st.text_input("Ticker da Ação", value="TAEE11")
        setor_acao = st.text_input("Setor da Empresa", value="Energia Elétrica / Utilidade Pública")
    with col2:
        hist_div = st.checkbox("Histórico consistente de dividendos?", value=True)

    if st.button("Analisar Ação"):
        acao_data = {
            "ticker": ticker_acao.upper(),
            "setor": setor_acao,
            "historico_dividendos_consistente": hist_div
        }
        resultado = AssetFilters.filtrar_acoes(acao_data)
        
        if resultado["aprovado"]:
            st.success(f"✅ A Ação **{resultado['ativo']}** foi **APROVADA** com base no perfil de dividendos/utilidade pública.")
        else:
            st.error(f"❌ A Ação **{resultado['ativo']}** foi **REPROVADA**.")
            for motivo in resultado["motivos"]:
                st.write(f"- {motivo}")

with tab3:
    st.subheader("Simulador de Filtro para Renda Fixa e Tesouro")
    col1, col2 = st.columns(2)
    with col1:
        nome_rf = st.text_input("Nome do Título", value="CDB Banco X (Vencimento 3 anos)")
        tipo_rf = st.selectbox("Tipo de Ativo", options=["cdb", "lci", "lca", "tesouro"])
    with col2:
        indexador_rf = st.selectbox("Indexador", options=["CDI", "IPCA", "SELIC", "PREFIXADO"])
        fgc_rf = st.checkbox("Possui cobertura do FGC?", value=True)

    if st.button("Analisar Renda Fixa"):
        rf_data = {
            "nome": nome_rf,
            "tipo": tipo_rf,
            "indexador": indexador_rf,
            "cobertura_fgc": fgc_rf
        }
        resultado = AssetFilters.filtrar_renda_fixa(rf_data)
        
        if resultado["aprovado"]:
            st.success(f"✅ O ativo **{resultado['ativo']}** atende aos critérios de segurança e indexação!")
        else:
            st.error(f"❌ O ativo **{resultado['ativo']}** foi **REPROVADO**.")
            for motivo in resultado["motivos"]:
                st.write(f"- {motivo}")
