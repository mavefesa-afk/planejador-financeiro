import json
import pandas as pd
from typing import Dict, Any, List

class ReportGenerator:
    """
    Módulo responsável por consolidar dados de portfólio e gerar estruturas
    prontas para exportação em relatórios executivos.
    """

    @staticmethod
    def gerar_dataframe_ativos(carteira: List[Dict[str, Any]]) -> pd.DataFrame:
        if not carteira:
            return pd.DataFrame(columns=["Ticker", "Classe", "Tipo", "Valor Atual"])
        return pd.DataFrame(carteira)

    @staticmethod
    def gerar_json_executivo(carteira: List[Dict[str, Any]], diagnostico: Dict[str, Any]) -> str:
        relatorio = {
            "sistema": "Planejador Financeiro — Brasil",
            "diagnostico_geral": diagnostico,
            "carteira_consolidada": carteira
        }
        return json.dumps(relatorio, indent=4, ensure_ascii=False)
