import streamlit as st
from core.database import DatabaseManager

st.set_page_config(page_title="Cadastrar Ativo - Planejador Financeiro", page_icon="➕", layout="wide")

st.title("➕ Cadastro de Ativos na Carteira (SQLite)")
st.markdown("Cadastre seus ativos reais. Eles serão salvos no banco de dados local e analisados automaticamente pelo diagnóstico.")

# Garante que o banco está inicializado
DatabaseManager.init_db()

with st.form("form_cadastro_ativo"):
    st.subheader("Informações Básicas")
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Ticker ou Nome do Ativo", placeholder="Ex: HGLG11, TAEE11 ou CDB XP")
        classe = st.selectbox("Classe de Ativo", options=["FII", "AÇÃO", "RENDA FIXA"])
    
    with col2:
        if classe == "FII":
            tipo = st.selectbox("Tipo de FII", options=["tijolo", "papel", "híbrido"])
        elif classe == "RENDA FIXA":
            tipo = st.selectbox("Tipo de Renda Fixa", options=["cdb", "lci", "lca", "tesouro"])
        else:
            tipo = "acao"
            st.text_input("Setor", value="Utilidade Pública / Energia", key="setor_acao_input")

    st.subheader("Parâmetros Quantitativos e de Risco")
    
    col3, col4 = st.columns(2)
    with col3:
        if classe == "FII":
            liquidez = st.number_input("Liquidez Diária Média (R$)", value=1000000.0, step=50000.0)
            p_vp = st.number_input("P/VP", value=0.95, step=0.01)
            vacancia = st.slider("Vacância (%)", 0.0, 50.0, 3.0) / 100.0
            dy_nominal = st.slider("DY Nominal (12m) (%)", 0.0, 25.0, 10.0) / 100.0
            
        elif classe == "AÇÃO":
            liquidez, p_vp, vacancia, dy_nominal = 0.0, 1.0, 0.0, 0.0
            hist_div = st.checkbox("Histórico consistente de dividendos?", value=True)
            
        else: # Renda Fixa
            liquidez, p_vp, vacancia, dy_nominal = 0.0, 1.0, 0.0, 0.0
            fgc = st.checkbox("Possui cobertura do FGC?", value=True)
            indexador = st.selectbox("Indexador", options=["CDI", "IPCA", "SELIC", "PREFIXADO"])

    submitted = st.form_submit_button("💾 Salvar Ativo no Banco de Dados")
    
    if submitted:
        if not ticker:
            st.error("Por favor, preencha o Ticker ou Nome do Ativo.")
        else:
            dados_novo_ativo = {
                "ticker": ticker,
                "classe": classe,
                "tipo": tipo,
                "setor": st.session_state.get("setor_acao_input", "Utilidade Pública") if classe == "AÇÃO" else "",
                "liquidez_diaria": locals().get("liquidez", 0.0),
                "p_vp": locals().get("p_vp", 1.0),
                "vacancia": locals().get("vacancia", 0.0),
                "dy_nominal_12m": locals().get("dy_nominal_12m", 0.0),
                "historico_dividendos_consistente": locals().get("hist_div", True),
                "cobertura_fgc": locals().get("fgc", True),
                "indexador": locals().get("indexador", "CDI")
            }
            DatabaseManager.adicionar_ativo(dados_novo_ativo)
            st.success(f"✅ Ativo **{ticker.upper()}** cadastrado com sucesso no SQLite!")

st.markdown("---")
st.subheader("📋 Ativos Atualmente Salvos no Banco de Dados")
carteira_atual = DatabaseManager.obtencao_carteira() if hasattr(DatabaseManager, 'obtencao_carteira') else DatabaseManager.obter_carteira()

if not carteira_atual:
    st.info("Nenhum ativo cadastrado até o momento.")
else:
    for ativo in carteira_atual:
        st.write(f"- **{ativo['ticker']}** ({ativo['classe']}) | Tipo: {ativo['tipo']}")

    if st.button("🗑️ Limpar Toda a Carteira"):
        DatabaseManager.limpar_carteira()
        st.warning("Banco de dados limpo com sucesso!")
        st.rerun()
