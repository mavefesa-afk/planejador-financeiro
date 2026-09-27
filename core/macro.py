from datetime import date
from typing import Dict, Any

class MacroScenario:
    """
    Módulo responsável por gerenciar o Cenário Macroecônomico do Brasil.
    Garante o registro de valores oficiais, datas e fontes, conforme o Contexto Mestre.
    """
    def __init__(self):
        # Dados estruturados com valor, data de referência e fonte oficial
        self._data = {
            "selic_anual": {
                "valor": 0.1125,  # Exemplo padrão inicial (11.25% a.a.) - deve ser atualizado com dados oficiais
                "data_referencia": "2026-09-01",
                "fonte": "Banco Central do Brasil (Copom)"
            },
            "ipca_12m": {
                "valor": 0.0450,  # Exemplo padrão inicial (4.50% a.a.)
                "data_referencia": "2026-08-31",
                "fonte": "IBGE (IPCA acumulado 12 meses)"
            }
        }

    def get_indicator(self, key: str) -> Dict[str, Any]:
        """Retorna o indicador completo com valor, data e fonte."""
        return self._data.get(key, {"valor": 0.0, "data_referencia": "N/D", "fonte": "N/D — dado não disponível"})

    def update_indicator(self, key: str, valor: float, data_referencia: str, fonte: str):
        """Atualiza um indicador macroeconômico garantindo rastreabilidade."""
        self._data[key] = {
            "valor": float(valor),
            "data_referencia": data_referencia,
            "fonte": fonte
        }

    def calcular_juro_real(self, taxa_nominal: Optional[float] = None) -> float:
        """
        Calcula o juro real utilizando a fórmula matematicamente correta:
        [(1 + taxa nominal) / (1 + inflação IPCA)] - 1
        Se taxa_nominal não for informada, utiliza a Selic atual.
        """
        nominal = taxa_nominal if taxa_nominal is not None else self._data["selic_anual"]["valor"]
        inflacao = self._data["ipca_12m"]["valor"]
        
        return ((1 + nominal) / (1 + inflacao)) - 1
