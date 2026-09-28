import sqlite3
from typing import List, Dict, Any

DB_NAME = "planejador.db"

def init_db():
    """Função global para inicializar o banco de dados e criar tabelas necessárias se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela de Ativos da Carteira
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carteira (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            classe TEXT NOT NULL,
            tipo TEXT,
            setor TEXT,
            liquidez_diaria REAL,
            p_vp REAL,
            vacancia REAL,
            dy_nominal_12m REAL,
            historico_dividendos_consistente INTEGER,
            cobertura_fgc INTEGER,
            indexador TEXT
        )
    """)
    
    conn.commit()
    conn.close()

class DatabaseManager:
    """
    Gerenciador do banco de dados SQLite para persistência dos ativos da carteira
    e parâmetros do Planejador Financeiro — Brasil.
    """

    @staticmethod
    def init_db():
        """Método de compatibilidade para inicializar o banco."""
        init_db()

    @staticmethod
    def adicionar_ativo(dados: Dict[str, Any]):
        """Insere um novo ativo na carteira do banco de dados."""
        init_db()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO carteira (
                ticker, classe, tipo, setor, liquidez_diaria, p_vp, 
                vacancia, dy_nominal_12m, historico_dividendos_consistente, 
                cobertura_fgc, indexador
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados.get("ticker", "").upper(),
            dados.get("classe", "").upper(),
            dados.get("tipo", "tijolo"),
            dados.get("setor", ""),
            dados.get("liquidez_diaria", 0.0),
            dados.get("p_vp", 1.0),
            dados.get("vacancia", 0.0),
            dados.get("dy_nominal_12m", 0.0),
            1 if dados.get("historico_dividendos_consistente", True) else 0,
            1 if dados.get("cobertura_fgc", True) else 0,
            dados.get("indexador", "CDI")
        ))
        
        conn.commit()
        conn.close()

    @staticmethod
    def obter_carteira() -> List[Dict[str, Any]]:
        """Busca todos os ativos cadastrados na carteira."""
        init_db()
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM carteira")
        rows = cursor.fetchall()
        conn.close()
        
        carteira = []
        for row in rows:
            carteira.append({
                "id": row["id"],
                "ticker": row["ticker"],
                "classe": row["classe"],
                "tipo": row["tipo"],
                "setor": row["setor"],
                "liquidez_diaria": row["liquidez_diaria"],
                "p_vp": row["p_vp"],
                "vacancia": row["vacancia"],
                "dy_nominal_12m": row["dy_nominal_12m"],
                "historico_dividendos_consistente": bool(row["historico_dividendos_consistente"]),
                "cobertura_fgc": bool(row["cobertura_fgc"]),
                "indexador": row["indexador"]
            })
            
        return carteira

    @staticmethod
    def limpar_carteira():
        """Remove todos os registros da carteira (útil para testes)."""
        init_db()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carteira")
        conn.commit()
        conn.close()
