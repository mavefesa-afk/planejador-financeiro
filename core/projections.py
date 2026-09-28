from typing import Dict, Any, List

class FinancialProjections:
    """
    Módulo de projeção de longo prazo e cálculo de Independência Financeira
    utilizando taxas de juros reais (juros compostos corrigidos pela inflação).
    """

    @staticmethod
    def projetar_independencia(
        patrimonio_atual: float, 
        aporte_mensal: float, 
        juro_real_anual: float, 
        renda_passiva_desejada_mensal: float
    ) -> Dict[str, Any]:
        """
        Calcula o tempo necessário (em meses/anos) para atingir o patrimônio alvo
        capaz de sustentar a renda passiva desejada com base no juro real.
        """
        if juro_real_anual <= 0:
            juro_real_anual = 0.01  # Evita divisão por zero ou taxas nulas/negativas extremas

        # Taxa real mensal equivalente
        r_mensal = (1 + juro_real_anual) ** (1 / 12) - 1

        # Patrimônio alvo necessário para gerar a renda desejada eternamente mantendo o poder de compra
        # Baseado na regra de que o rendimento real anual cobre a renda passiva anual:
        # Patrimonio * Juro Real Anual = Renda Passiva Anual
        patrimonio_alvo = (renda_passiva_desejada_mensal * 12) / juro_real_anual

        patrimonio = patrimonio_atual
        meses = 0
        trajetoria = []

        # Simulação mês a mês (limite de segurança de 100 anos = 1200 meses)
        while patrimonio < patrimonio_alvo and meses < 1200:
            rendimento_mes = patrimonio * r_mensal
            patrimonio = patrimonio + rendimento_mes + aporte_mensal
            meses += 1
            
            if meses % 12 == 0:
                trajetoria.append({
                    "ano": meses // 12,
                    "patrimonio": patrimonio
                })

        anos = meses // 12
        meses_restantes = meses % 12
        alcancavel = meses < 1200

        return {
            "patrimonio_alvo": patrimonio_alvo,
            "meses_totais": meses,
            "anos": anos,
            "meses_restantes": meses_restantes,
            "patrimonio_final": patrimonio,
            "alcancavel": alcancavel,
            "trajetoria": trajetoria
        }
