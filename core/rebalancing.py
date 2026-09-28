from typing import Dict, Any, List

class PortfolioRebalancing:
    """
    Módulo responsável por calcular o desvio entre a alocação atual da carteira
    e a alocação alvo desejada, recomendando o direcionamento de novos aportes.
    """

    @staticmethod
    def calcular_rebalanceamento(
        patrimonio_por_classe: Dict[str, float], 
        alocacao_alvo_percentual: Dict[str, float], 
        aporte_disponivel: float
    ) -> Dict[str, Any]:
        """
        Calcula o patrimônio total, os percentuais atuais, as diferenças em relação
        ao alvo e quanto do novo aporte deve ir para cada classe de ativo.
        """
        patrimonio_total = sum(patrimonio_por_classe.values())
        
        # Se a carteira estiver zerada, distribui o aporte 100% com base no alvo ideal
        if patrimonio_total <= 0:
            recomendacoes = {}
            for classe, alvo in alocacao_alvo_percentual.items():
                recomendacoes[classe] = aporte_disponivel * alvo
            return {
                "patrimonio_total": 0.0,
                "status_por_classe": {c: {"atual_pct": 0.0, "alvo_pct": alvo * 100, "valor_atual": 0.0} for c, alvo in alocacao_alvo_percentual.items()},
                "recomendacao_aporte": recomendacoes
            }

        status_por_classe = {}
        soma_desvios_negativos = 0.0
        desvios = {}

        # 1. Analisa o estado atual versus o alvo
        for classe, alvo_pct in alocacao_alvo_percentual.items():
            valor_atual = patrimonio_por_classe.get(classe, 0.0)
            atual_pct = valor_atual / patrimonio_total
            desvio = atual_pct - alvo_pct  # Positivo = acima do alvo; Negativo = abaixo do alvo
            
            desvios[classe] = desvio
            status_por_classe[classe] = {
                "valor_atual": valor_atual,
                "atual_pct": atual_pct * 100,
                "alvo_pct": alvo_pct * 100,
                "desvio_pct": desvio * 100
            }

            if desvio < 0:
                soma_desvios_negativos += abs(desvio)

        # 2. Calcula o direcionamento do aporte para as classes que estão abaixo do alvo
        recomendacoes = {}
        patrimonio_futuro = patrimonio_total + aporte_disponivel

        for classe, alvo_pct in alocacao_alvo_percentual.items():
            valor_atual = patrimonio_por_classe.get(classe, 0.0)
            valor_alvo_futuro = patrimonio_futuro * alvo_pct
            
            # Quanto falta para atingir o valor alvo ideal no cenário futuro
            necessario = valor_alvo_futuro - valor_atual
            
            # Garante que não recomendaremos valores negativos se a classe estiver muito acima do alvo
            recomendacao = max(0.0, necessario)
            recomendacoes[classe] = recomendacao

        # Caso a soma das recomendações supere o aporte (por arredondamentos ou sobre-alocações), ajusta proporcionalmente
        soma_rec = sum(recomendacoes.values())
        if soma_rec > 0 and soma_rec != aporte_disponivel:
            fator = aporte_disponivel / soma_rec
            for classe in recomendacoes:
                recomendacoes[classe] *= fator

        return {
            "patrimonio_total": patrimonio_total,
            "status_por_classe": status_por_classe,
            "recomendacao_aporte": recomendacoes
        }
