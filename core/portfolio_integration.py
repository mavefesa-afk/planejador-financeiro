from typing import Dict, Any, List
from core.filters import AssetFilters

class PortfolioIntegration:
    """
    Módulo responsável por cruzar a carteira atual do usuário com o motor de filtros
    e regras macroeconômicas, gerando diagnósticos e recomendações de alocação.
    """

    @staticmethod
    def analisar_carteira(ativos_carteira: List[Dict[str, Any]], ipca_12m: float) -> Dict[str, Any]:
        """
        Analisa uma lista de ativos da carteira atual aplicando os filtros correspondentes
        a cada classe (FII, Ação, Renda Fixa).
        """
        resultados = []
        aprovados_count = 0
        reprovados_count = 0

        for ativo in ativos_carteira:
            classe = ativo.get("classe", "").upper()
            analise = {"ativo": ativo.get("ticker", ativo.get("nome", "Desconhecido")), "classe": classe}

            if classe == "FII":
                res_filtro = AssetFilters.filtrar_fiis(ativo, ipca_12m)
                analise.update(res_filtro)
            elif classe == "AÇÃO" or classe == "ACOES":
                res_filtro = AssetFilters.filtrar_acoes(ativo)
                analise.update(res_filtro)
            elif classe == "RENDA FIXA" or classe == "RF":
                res_filtro = AssetFilters.filtrar_renda_fixa(ativo)
                analise.update(res_filtro)
            else:
                analise["aprovado"] = True
                analise["motivos"] = ["Classe genérica ou não restrita por filtros automáticos."]

            if analise.get("aprovado", False):
                aprovados_count += 1
            else:
                reprovados_count += 1

            resultados.append(analise)

        return {
            "total_analisados": len(ativos_carteira),
            "aprovados": aprovados_count,
            "reprovados": reprovados_count,
            detalhes: resultados
        }
