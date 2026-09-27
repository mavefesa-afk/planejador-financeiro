from typing import Dict, Any, List

class AssetFilters:
    """
    Módulo de Filtragem e Seleção de Ativos (FIIs, Ações, Renda Fixa e Tesouro)
    baseado estritamente nas regras e critérios definidos no Contexto Mestre.
    """

    @staticmethod
    def filtrar_fiis(fii: Dict[str, Any], ipca_12m: float) -> Dict[str, Any]:
        """
        1. FIIs (Fundos Imobiliários):
           - Gestão por empresas grandes / histórico sólido.
           - Liquidez diária > R$ 700.000,00.
           - P/VP < 1.00 (especialmente para fundos de tijolo).
           - Vacância < 5% (para tijolo).
           - DY Real calculado > 5% a.a. (com base nos últimos 12 meses).
        """
        razoes_reprovacao = []
        
        # Liquidez Diária
        liquidez = fii.get("liquidez_diaria", 0.0)
        if liquidez < 700000.0:
            razoes_reprovacao.append(f"Liquidez diária abaixo de R$ 700k (Atual: R$ {liquidez:,.2f})")

        # P/VP (Aplicável a tijolo)
        tipo = fii.get("tipo", "tijolo").lower()
        p_vp = fii.get("p_vp", 1.0)
        if tipo == "tijolo" and p_vp >= 1.00:
            razoes_reprovacao.append(f"P/VP igual ou superior a 1.00 para fundo de tijolo (Atual: {p_vp})")

        # Vacância (Aplicável a tijolo)
        vacancia = fii.get("vacancia", 0.0)
        if tipo == "tijolo" and vacancia >= 0.05:
            razoes_reprovacao.append(f"Vacância acima de 5% (Atual: {vacancia * 100:.1f}%)")

        # DY Real (Fórmula correta: [(1 + DY Nominal) / (1 + IPCA)] - 1)
        dy_nominal = fii.get("dy_nominal_12m", 0.0)
        dy_real = ((1 + dy_nominal) / (1 + ipca_12m)) - 1
        
        if dy_real < 0.05:
            razoes_reprovacao.append(f"DY Real abaixo de 5% a.a. (Atual: {dy_real * 100:.2f}%)")

        aprovado = len(razoes_reprovacao) == 0
        
        return {
            "ativo": fii.get("ticker", "DESCONHECIDO"),
            "classe": "FII",
            "aprovado": aprovado,
            "dy_real": dy_real,
            "motivos": razoes_reprovacao
        }

    @staticmethod
    def filtrar_acoes(acao: Dict[str, Any]) -> Dict[str, Any]:
        """
        2. Ações:
           - Foco em empresas pagadoras de dividendos sólidos.
           - Foco em empresas de utilidade pública (energia, saneamento, etc.).
        """
        setor = acao.get("setor", "").lower()
        pagadora_dividendos = acao.get("historico_dividendos_consistente", False)
        
        setores_utilidade = ["utilidade pública", "energia", "saneamento", "segurança", "bancos sólidos"]
        eh_utilidade_publica = any(s in setor for s in setores_utilidade)

        razoes_reprovacao = []
        if not pagadora_dividendos:
            razoes_reprovacao.append("Não possui histórico consistente de pagamentos de dividendos.")
        if not eh_utilidade_publica and setor not in ["bancos", "telecomunicações"]:
            razoes_reprovacao.append(f"Setor ({acao.get('setor', 'Desconhecido')}) fora do perfil focado em utilidade pública/dividendos.")

        aprovado = len(razoes_reprovacao) == 0

        return {
            "ativo": acao.get("ticker", "DESCONHECIDO"),
            "classe": "Ações",
            "aprovado": aprovado,
            "motivos": razoes_reprovacao
        }

    @staticmethod
    def filtrar_renda_fixa(ativo_rf: Dict[str, Any]) -> Dict[str, Any]:
        """
        3. Renda Fixa (CDBs, LCIs/LCAs, Tesouro Direto):
           - Cobertura obrigatória do FGC (para emissões bancárias).
           - Pós-fixados atrelados ao CDI ou IPCA+ com taxas reais garantidas.
           - Estratégia de liquidez diária ou pagamento de juros semestrais/mensais.
        """
        razoes_reprovacao = []
        
        possui_fgc = ativo_rf.get("cobertura_fgc", True)
        tipo_emissao = ativo_rf.get("tipo", "").lower() # ex: cdb, lci, lca, tesouro
        
        if tipo_emissao in ["cdb", "lci", "lca"] and not possui_fgc:
            razoes_reprovacao.append("Ativo de renda fixa privada sem cobertura do FGC.")

        indexador = ativo_rf.get("indexador", "").upper() # CDI, IPCA
        if indexador not in ["CDI", "IPCA", "SELIC"]:
            razoes_reprovacao.append(f"Indexador inválido ou fora da estratégia ({indexador}).")

        aprovado = len(razoes_reprovacao) == 0

        return {
            "ativo": ativo_rf.get("nome", "DESCONHECIDO"),
            "classe": "Renda Fixa / Tesouro",
            "aprovado": aprovado,
            "motivos": razoes_reprovacao
        }
