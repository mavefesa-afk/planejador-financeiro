from typing import Dict, Any

class FinancialCalculations:
    """
    Módulo de cálculos financeiros determinísticos para o Planejador Financeiro — Brasil.
    """

    @staticmethod
    def calcular_aliquota_ir(dias_investido: int) -> float:
        """
        Retorna a alíquota de Imposto de Renda regressiva para Renda Fixa:
        - Até 180 dias: 22.5%
        - De 181 a 360 dias: 20.0%
        - De 361 a 720 dias: 17.5%
        - Acima de 720 dias: 15.0%
        """
        if dias_investido <= 180:
            return 0.225
        elif dias_investido <= 360:
            return 0.20
        elif dias_investido <= 720:
            return 0.175
        else:
            return 0.15

    @staticmethod
    def calcular_rendimento_liquido(valor_aplicado: float, valor_bruto: float, dias_investido: int) -> Dict[str, Any]:
        """
        Calcula o lucro líquido de um ativo de renda fixa após a incidência do IR regressivo.
        """
        lucro_bruto = valor_bruto - valor_aplicado
        
        if lucro_bruto <= 0:
            return {
                "lucro_bruto": 0.0,
                "aliquota_ir": 0.0,
                "imposto_devido": 0.0,
                "valor_liquido": valor_bruto,
                "lucro_liquido": 0.0
            }

        aliquota_ir = FinancialCalculations.calcular_aliquota_ir(dias_investido)
        imposto_devido = lucro_bruto * aliquota_ir
        lucro_liquido = lucro_bruto - imposto_devido
        valor_liquido = valor_aplicado + lucro_liquido

        return {
            "lucro_bruto": lucro_bruto,
            "aliquota_ir": aliquota_ir,
            "imposto_devido": imposto_devido,
            "valor_liquido": valor_liquido,
            "lucro_liquido": lucro_liquido
        }
