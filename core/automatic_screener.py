from typing import Dict, Any, List

class AutomaticScreener:
    """
    Motor de varredura e triagem automática de ativos com base estrita
    nos critérios quantitativos e qualitativos definidos pelo usuário.
    """

    @staticmethod
    def filtrar_fiis(lista_ativos: List[Dict[str, Any]], ipca_atual: float) -> List[Dict[str, Any]]:
        aprovados = []
        for ativo in lista_ativos:
            if ativo.get("classe") != "FII":
                continue
            
            tipo = ativo.get("tipo", "").lower()
            dy = ativo.get("dy_nominal_12m", 0.0)
            p_vp = ativo.get("p_vp", 1.0)
            liq = ativo.get("liquidez_diaria", 0.0)
            pl = ativo.get("patrimonio_liquido", 0.0)
            
            alerta_outlier = dy > 0.135
            yield_real = dy - ipca_atual
            
            motivos_reprovacao = []
            
            # Liquidez e Tamanho (Comuns)
            if liq < 1000000:
                motivos_reprovacao.append("Liquidez diária abaixo de R$ 1 Milhão")
            if pl < 500000000:
                motivos_reprovacao.append("Patrimônio Líquido abaixo de R$ 500 Milhões")

            if tipo == "tijolo":
                if not (0.085 <= dy <= 0.10) and not alerta_outlier:
                    motivos_reprovacao.append("DY fora da faixa ideal de Tijolo (8.5% a 10%)")
                if p_vp > 1.0:
                    motivos_reprovacao.append("P/VP superior a 1.0 para Tijolo")
                if ativo.get("vacancia_fisica", 0.0) >= 0.10:
                    motivos_reprovacao.append("Vacância física igual ou superior a 10%")
                if ativo.get("qtd_imoveis", 0) <= 5:
                    motivos_reprovacao.append("Risco de monoativo (Qtd imóveis <= 5)")
                if not ativo.get("multi_inquilinos", True):
                    motivos_reprovacao.append("Fundo monolocatário")

            elif tipo == "papel":
                if not (0.11 <= dy <= 0.125) and not alerta_outlier:
                    motivos_reprovacao.append("DY fora da faixa ideal de Papel (11% a 12.5%)")
                if p_vp > 1.03:
                    motivos_reprovacao.append("P/VP superior a 1.03 para Papel")
                if ativo.get("rating_credito", "") not in ["High Grade", "AAA", "AA"]:
                    motivos_reprovacao.append("Rating de crédito fora do padrão High Grade")

            status = {
                "ticker": ativo.get("ticker"),
                "tipo": tipo,
                "dy_nominal": dy * 100,
                "yield_real": yield_real * 100,
                "alerta_outlier": alerta_outlier,
                "aprovado": len(motivos_reprovacao) == 0,
                "motivos": motivos_reprovacao
            }
            aprovados.append(status)
        return aprovados

    @staticmethod
    def filtrar_renda_fixa(lista_ativos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        aprovados = []
        for ativo in lista_ativos:
            if ativo.get("classe") != "RENDA FIXA":
                continue
            
            tipo = ativo.get("tipo", "").lower()
            taxa_cdi_pct = ativo.get("taxa_cdi_percentual", 1.0) # ex: 1.05 para 105% do CDI
            fgc = ativo.get("cobertura_fgc", False)
            rating = ativo.get("rating_emissor", "A")
            pagamento_mensal = ativo.get("pagamento_mensal", False)
            prazo_anos = ativo.get("prazo_anos", 2.0)
            
            motivos = []
            if not fgc:
                motivos.append("Sem cobertura do FGC (Risco de crédito descoberto)")
            if rating not in ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-"]:
                motivos.append("Rating do emissor abaixo de A-")
            if not pagamento_mensal:
                motivos.append("Não possui fluxo de caixa mensal obrigatório (juros periódicos)")
            if not (1.0 <= prazo_anos <= 5.0):
                motivos.append("Prazo fora da faixa alvo (1 a 5 anos)")

            if tipo == "cdb":
                if not (1.0 <= taxa_cdi_pct <= 1.10):
                    motivos.append("CDB fora da faixa alvo (100% a 110% do CDI)")
            elif tipo in ["lci", "lca"]:
                if not (0.85 <= taxa_cdi_pct <= 0.95):
                    motivos.append("LCI/LCA fora da faixa alvo (85% a 95% do CDI)")

            status = {
                "ticker": ativo.get("ticker"),
                "tipo": tipo.upper(),
                "taxa": f"{taxa_cdi_pct * 100:.1f}% do CDI",
                "aprovado": len(motivos) == 0,
                "motivos": motivos
            }
            aprovados.append(status)
        return aprovados

    @staticmethod
    def filtrar_etfs(lista_ativos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        aprovados = []
        for ativo in lista_ativos:
            if ativo.get("classe") != "ETF":
                continue
            
            distribui = ativo.get("distribui_dividendos", False)
            periodicidade = ativo.get("periodicidade", "").lower()
            dy = ativo.get("dy_nominal_12m", 0.0)
            tx_adm = ativo.get("taxa_administracao", 0.005)
            liq = ativo.get("liquidez_diaria", 0.0)
            aum = ativo.get("patrimonio_liquido_aum", 0.0)
            
            alerta_outlier = dy > 0.15
            motivos = []

            if not distribui or periodicidade != "mensal":
                motivos.append("ETF não distribui dividendos com periodicidade mensal")
            if not (0.07 <= dy <= 0.11) and not alerta_outlier:
                motivos.append("DY fora da faixa ideal (7% a 11% a.a.)")
            if tx_adm > 0.01:
                motivos.append("Taxa de administração superior a 1% a.a.")
            if liq < 1000000:
                motivos.append("Liquidez diária abaixo de R$ 1 Milhão/dia")
            if aum < 100000000:
                motivos.append("Patrimônio Líquido (AUM) abaixo de R$ 100 Milhões")

            status = {
                "ticker": ativo.get("ticker"),
                "dy": dy * 100,
                "alerta_outlier": alerta_outlier,
                "aprovado": len(motivos) == 0,
                "motivos": motivos
            }
            aprovados.append(status)
        return aprovados
