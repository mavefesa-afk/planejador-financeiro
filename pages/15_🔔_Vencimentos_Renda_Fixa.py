import streamlit as st
from core.database import DatabaseManager
from core.maturities import MaturityTracker

st.set_page_config(page_title="Vencimentos de Renda Fixa - Planejador Financeiro", page_icon="🔔", layout="wide")

st.title("🔔 Monitor de Vencimentos e Reinvestimentos (Renda Fixa)")
st.markdown("Acompanhe o prazo de vencimento dos seus títulos de renda fixa para planejar o resgate ou o reinvestimento antecipado.")

# Amostra de teste ou busca do banco
carteira = DatabaseManager.obter_carteira()

# Filtrando ou simulando dados para demonstração caso o usuário não tenha cadastrado datas de vencimento ainda
ativos_rf = [a for a in carteira if a.get("classe") == "RENDA FIXA"]

if not ativos_rf:
    st.info("💡 Nenhum título de Renda Fixa cadastrado na carteira SQLite. Exibindo demonstrativo padrão de monitoramento:")
    ativos_rf = [
        {"ticker": "CDB Banco Inter 110% CDI", "classe": "RENDA FIXA", "vencimento": "2026-11-15"},
        {"ticker": "Tesouro IPCA+ 2028", "classe": "RENDA FIXA", "vencimento": "2028-08-15"},
        {"ticker": "LCI Banco ABC 92% CDI", "classe": "RENDA FIXA", "vencimento": "2026-07-10"}
    ]

vencimentos = MaturityTracker.verificar_vencimentos(ativos_rf)

st.subheader("📋 Status de Vencimento dos Títulos")

for item in vencimentos:
    dias = item["dias_restantes"]
    if dias < 0:
        icone = "❌"
        msg = f"Título VENCIDO há {abs(dias)} dias!"
    elif item["alerta_reinvestimento"]:
        icone = "⚠️"
        msg = f"Vence em breve ({dias} dias restantes). Prepare o reinvestimento!"
    else:
        icone = "✅"
        msg = f"Prazo saudável ({dias} dias restantes)."

    with st.expander(f"{icone} {item['ticker']} — Vencimento: {item['vencimento']}"):
        st.write(f"- **Status:** {msg}")
        if item["alerta_reinvestimento"] or dias < 0:
            st.warning("💡 **Dica da Estratégia:** Pesquise novas taxas no mercado para alocar o montante principal + rendimento líquido.")
        else:
            st.success("O título está rendendo conforme planejado no horizonte de longo prazo.")
