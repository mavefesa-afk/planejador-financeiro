from datetime import datetime, date
from typing import Dict, Any, List

class MaturityTracker:
    """
    Módulo para monitoramento de prazos de vencimento de títulos de Renda Fixa.
    """

    @staticmethod
    def verificar_vencimentos(ativos_rf: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerta_vencimentos = []
        hoje = date.today()
        
        for ativo in ativos_rf:
            if ativo.get("classe") != "RENDA FIXA":
                continue
                
            venc_str = ativo.get("vencimento", "2028-12-31")
            try:
                dt_venc = datetime.strptime(venc_str, "%Y-%m-%d").date()
                dias_restantes = (dt_venc - hoje).days
            except Exception:
                dias_restantes = 365
            
            # Alerta se vencer em menos de 180 dias (6 meses)
            status = {
                "ticker": ativo.get("ticker", "Título RF"),
                "vencimento": venc_str,
                "dias_restantes": dias_restantes,
                "alerta_reinvestimento": dias_restantes <= 180
            }
            alerta_vencimentos.append(status)
            
        return alerta_vencimentos
