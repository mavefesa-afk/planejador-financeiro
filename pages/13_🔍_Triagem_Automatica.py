import streamlit as st
from core.macro import MacroScenario
from core.database import DatabaseManager
from core.automatic_screener import AutomaticScreener

st.set_page_config(page_title="Triagem Automática - Planejador Financeiro", page_icon="🔍", layout="wide")

st.title("🔍 Módulo de Triagem Inteligente de Mercado")
st.markdown("Escolha como deseja alimentar e analisar o seu portfólio: via inserção manual de ativos ou executando a varredura automática com base nos parâmetros rígidos da estratégia.")

modo_entrada = st.radio(
    "Selecione o modo de operação:",
    options=["Inserir Manualmente (Banco de Dados Local)", "Executar Busca / Varredura Automática de Mercado"],
    horizontal=True
)

macro = MacroScenario()
ipca_atual = macro.get_indicator("ipca_12m")["valor"]

if modo_entrada == "Inserir Manualmente (Banco de Dados Local)":
    st.info("💡 Você está utilizando os ativos cadastrados manualmente no seu SQLite. Acesse a página **Cadastrar Ativo** para adicionar novos itens.")
    carteira = DatabaseManager.obter_carteira()
    
    if not carteira:
        st.warning("Nenhum ativo cadastrado no banco de dados.")
    else:
        st.subheader("Ativos Cadastrados Atualmente")
        for at in carteira:
            st.write(f"- **{at['ticker']}** ({at['classe']}) | Tipo: {at['tipo']}")

else:
    st.subheader("🤖 Varredura Automática Baseada em Critérios Quantitativos")
    st.markdown(f"**Cenário de Referência:** IPCA Acumulado 12m: **{ipca_atual * 100:.2f}% a.a.**")
    
    # Base de dados simulada de mercado representativa para demonstração do motor de triagem
    mercado_amostra = [
        # FIIs Tijolo
        {"ticker": "HGLG11", "classe": "FII", "tipo": "tijolo", "dy_nominal_12m": 0.092, "p_vp": 0.98, "vacancia_fisica": 0.04, "qtd_imoveis": 18, "multi_inquilinos": True, "liquidez_diaria": 4500000.0, "patrimonio_liquido": 5200000000.0},
        {"ticker": "XPML11", "classe": "FII", "tipo": "tijolo", "dy_nominal_12m": 0.145, "p_vp": 1.02, "vacancia_fisica": 0.02, "qtd_imoveis": 16, "multi_inquilinos": True, "liquidez_diaria": 8000000.0, "patrimonio_liquido": 3800000000.0}, # Outlier DY > 13.5%
        # FIIs Papel
        {"ticker": "KNIP11", "classe": "FII", "tipo": "papel", "dy_nominal_12m": 0.118, "p_vp": 1.01, "rating_credito": "High Grade", "liquidez_diaria": 6000000.0, "patrimonio_liquido": 6500000000.0},
        # Renda Fixa
        {"ticker": "CDB XP 110% CDI", "classe": "RENDA FIXA", "tipo": "cdb", "taxa_cdi_percentual": 1.10, "cobertura_fgc": True, "rating_emissor": "AAA", "pagamento_mensal": True, "prazo_anos": 3.0},
        {"ticker": "LCI Banco X 90% CDI", "classe": "RENDA FIXA", "tipo": "lci", "taxa_cdi_percentual": 0.90, "cobertura_fgc": True, "rating_emissor": "AA", "pagamento_mensal": True, "prazo_anos": 2.0},
        # ETFs
        {"ticker": "NDIV11", "classe": "ETF", "distribui_dividendos": True, "periodicidade": "mensal", "dy_nominal_12m": 0.085, "taxa_administracao": 0.004, "liquidez_diaria": 2500000.0, "patrimonio_liquido_aum": 200000000.0}
    ]

    if st.button("🚀 Executar Varredura Automática de Ativos"):
        res_fiis = AutomaticScreener.filtrar_fiis(mercado_amostra, ipca_atual)
        res_rf = AutomaticScreener.filtrar_renda_fixa(mercado_amostra)
        res_etfs = AutomaticScreener.filtrar_etfs(mercado_amostra)

        st.markdown("---")
        st.subheader("📊 Resultados da Varredura Automática")

        tab1, tab2, tab3 = st.tabs(["FIIs (Tijolo & Papel)", "Renda Fixa", "ETFs de Dividendos"])

        with tab1:
            st.markdown("### Fundos Imobiliários")
            for item in res_fiis:
                with st.expander(f"{'✅' if item['aprovado'] else '⚠️'} {item['ticker']} ({item['tipo'].upper()})"):
                    st.write(f"- **DY Nominal:** {item['dy_nominal']:.2f}% a.a. | **Yield Real:** {item['yield_real']:.2f}% a.a.")
                    if item["alerta_outlier"]:
                        st.warning("⚠️ **Alerta Outlier:** DY superior a 13.5% sinaliza risco elevado ou dividendo não recorrente.")
                    if item["aprovado"]:
                        st.success("Ativo aprovado com base nos critérios de liquidez, P/VP e vacância.")
                    else:
                        st.error("Ativo reprovado pelos seguintes motivos:")
                        for m in item["motivos"]:
                            st.write(f"  - {m}")

        with tab2:
            st.markdown("### Renda Fixa (CDB / LCI / LCA)")
            for item in res_rf:
                with st.expander(f"{'✅' if item['aprovado'] else '⚠️'} {item['ticker']}"):
                    st.write(f"- **Rentabilidade:** {item['taxa']}")
                    if item["aprovado"]:
                        st.success("Título em conformidade com as regras de FGC, rating, prazo e juros mensais.")
                    else:
                        st.error("Desvios identificados:")
                        for m in item["motivos"]:
                            st.write(f"  - {m}")

        with tab3:
            st.markdown("### ETFs de Distribuição Mensal")
            for item in res_etfs:
                with st.expander(f"{'✅' if item['aprovado'] else '⚠️'} {item['ticker']}"):
                    st.write(f"- **DY 12m:** {item['dy']:.2f}% a.a.")
                    if item["alerta_outlier"]:
                        st.warning("⚠️ **Alerta Outlier:** DY superior a 15% (Estratégia sintética/derivativos).")
                    if item["aprovado"]:
                        st.success("ETF aprovado conforme as regras de custo, liquidez e AUM.")
                    else:
                        st.error("Motivos de reprovação:")
                        for m in item["motivos"]:
                            st.write(f"  - {m}")
