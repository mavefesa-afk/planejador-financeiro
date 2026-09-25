# Planejador Financeiro — Brasil

Aplicativo inicial em Python + Streamlit + SQLite para planejamento financeiro e aposentadoria.

## Objetivo

Criar, em etapas, um sistema que:

- cadastra perfil financeiro;
- cadastra carteira;
- registra cenário macroeconômico;
- calcula alocação;
- projeta patrimônio;
- calcula taxa de retirada;
- gera relatório.

## Tecnologias

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Instalação local

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Depois:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Importante

Esta é a fundação do projeto. Ela ainda NÃO deve ser considerada um sistema financeiro final.

As próximas versões devem integrar:

1. fontes oficiais de Selic/IPCA;
2. dados de mercado da B3 e/ou fontes confiáveis;
3. catálogo de FIIs;
4. catálogo de ETFs;
5. regras tributárias versionadas;
6. importação da carteira via CSV/XLSX;
7. motor de scoring;
8. rebalanceamento;
9. simulação Monte Carlo;
10. geração de relatório;
11. camada opcional de IA.

## Arquitetura

```text
planejador_financeiro/
├── app.py
├── core/
│   ├── calculations.py
│   ├── config.py
│   ├── database.py
│   ├── profile.py
│   ├── portfolio.py
│   ├── allocation.py
│   ├── tax.py
│   └── report.py
├── pages/
│   ├── 01_👤_Perfil.py
│   ├── 02_💼_Carteira_Atual.py
│   ├── 03_🌎_Cenário_Macro.py
│   ├── 04_🎯_Alocação.py
│   ├── 05_📈_Projeções.py
│   └── 06_📄_Relatório.py
├── data/
├── .streamlit/
├── requirements.txt
└── README.md
```
