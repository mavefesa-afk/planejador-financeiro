import streamlit as st
from core.database import DatabaseManager
from core.rebalancing import PortfolioRebalancing

st.set_page_config(page_title="Rebalanceamento de Carteira - Planejador Financeiro", page_icon="⚖️", layout="wide")

st.title("⚖️ Rebalanceamento Inteligente de Carteira")
st.markdown("Compare a alocação atual dos seus ativos cadastrados no banco de dados com a sua estratégia alvo e descubra onde aplicar os próximos aportes.")

# 1. Carrega os ativos da carteira do SQLite
carteira_db = DatabaseManager.obter_carteira()

# Agrupa o patrimônio por classe (Exemplo simplificado: agrupando por classe cadastrada)
# Nota: Como o cadastro atual foca em regras/parâmetros, simulamos valores ou assumimos pesos padrão caso não haja valor financeiro explícito cadastrado.
st.subheader("1. Defina sua Alocação Alvo (Estratégia Ideal)")
col_alvo1, col_alvo2, col_alvo3 = st.columns(3)

with col_alvo1:
    alvo_fii = st.number_input("Alvo FIIs (%)", value=40.0, step=1.0) / 100.0
with col_alvo2:
    alvo_acao = st.number_input("Alvo Ações (%)", value=30.0, step=1.0) / 100.0
with col_alvo3:
    alvo_rf = st.number_input("Alvo Renda Fixa (%)", value=30.0, step=1.0) / 100.0

soma_alvos = alvo_fii + alvo_acao + alvo_rf
if abs(soma_alvos - 1.0) > 0.001:
    st.warning(f"⚠️ A soma dos alvos atuais é {soma_alvos * 100:.1f}%. O ideal é que feche exatamente em 100%.")

st.subheader("2. Informe o Valor Atual por Classe e o Novo Aporte")
col_val1, col_val2, col_val3 = st.columns(3)

with col_val1:
    val_fii = st.number_input("Patrimônio Atual em FIIs (R$)", value=40000.0, step=1000.0)
with col_val2:
    val_acao = st.number_input("Patrimônio Atual em Ações (R$)", value=30000.0, step=1000.0)
with col_val3:
    val_rf = st.number_input("Patrimônio Atual em Renda Fixa (R$)", value=30000.0, step=1000.0)

aporte_mes = st.number_input("Valor do Novo Aporte Disponível (R$)", value=5000.0, step=500.0)

if st.button("⚖️ Calcular Rebalanceamento e Direcionamento"):
    patrimonio_por_classe = {
        "FII": val_fii,
        "AÇÃO": val_acao,
        "RENDA FIXA": val_rf
    }
    alocacao_alvo = {
        "FII": alvo_fii,
        "AÇÃO": alvo_acao,
        "RENDA FIXA": alvo_rf
    }

    resultado = PortfolioRebalancing.calcular_rebalanceamento(
        patrimonio_por_classe=patrimonio_por_classe,
        alocacao_alvo_percentual=alocacao_alvo,
        aporte_disponivel=aporte_mes
    )

    st.markdown("---")
    st.subheader("📊 Diagnóstico de Desvio de Alocação")
    
    st.metric("Patrimônio Total Atual", f"R$ {resultado['patrimonio_total']:,.2f}")

    col_res1, col_res2, col_res3 = st.columns(3)
    
    status = resultado["status_por_classe"]
    
    with col_res1:
        st.write("**Fundos Imobiliários (FIIs)**")
        st.write(f"- Atual: **{status['FII']['atual_pct']:.1f}%** (Alvo: {status['FII']['alvo_pct']:.1f}%)")
        st.write(f"- Desvio: {status['FII']['desvio_pct']:+.1f}%")

    with col_res2:
        st.write("**Ações**")
        st.write(f"- Atual: **{status['AÇÃO']['atual_pct']:.1f}%** (Alvo: {status['AÇÃO']['alvo_pct']:.1f}%)")
        st.write(f"- Desvio: {status['AÇÃO']['desvio_pct']:+.1f}%")

    with col_res3:
        st.write("**Renda Fixa**")
        st.write(f"- Atual: **{status['RENDA FIXA']['atual_pct']:.1f}%** (Alvo: {status['RENDA FIXA']['alvo_pct']:.1f}%)")
        st.write(f"- Desvio: {status['RENDA FIXA']['desvio_pct']:+.1f}%")

    st.markdown("---")
    st.subheader("💡 Onde Aplicar o Novo Aporte (R$ {:,.2f})".format(aporte_mes))
    
    rec = resultado["recomendacao_aporte"]
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    
    col_rec1.metric("Aporte em FIIs", f"R$ {rec.get('FII', 0.0):,.2f}")
    col_rec2.metric("Aporte em Ações", f"R$ {rec.get('AÇÃO', 0.0):,.2f}")
    col_rec3.metric("Aporte em Renda Fixa", f"R$ {rec.get('RENDA FIXA', 0.0):,.2f}")
    
    st.success("✅ Siga esta distribuição para aproximar organicamente a sua carteira da sua estratégia-alvo de longo prazo!")
