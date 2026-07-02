# Análise Exploratória de Dados — Tesouro Direto

Pipeline de ETL e análise exploratória sobre o histórico de preços e taxas
dos títulos públicos do Tesouro Direto, com geração automática de gráficos
e insights de negócio.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Objetivos](#objetivos)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Como rodar](#como-rodar)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Insights encontrados](#insights-encontrados)

---

## Sobre o projeto

Dados públicos do governo costumam vir brutos, inconsistentes e sem padronização
(encoding, separadores, nomes de coluna). Este projeto resolve isso com um pipeline
modular, testado e versionado, que transforma o histórico de 170k+ registros do
Tesouro Direto em análises prontas para decisão.

## Objetivos

- Mapear a evolução das taxas por tipo de título ao longo do tempo
- Calcular o spread médio (compra vs. venda) por título, como proxy de liquidez
- Identificar padrões de sazonalidade mensal nas taxas
- Gerar insights de negócio automaticamente a partir dos dados

## Arquitetura
data/raw (.csv) → ingestion.py → cleaning.py → analysis.py → visualization.py / insights.py → outputs/

Pipeline ETL clássico: cada módulo tem responsabilidade única (ingestão, limpeza,
análise, visualização), comunicando-se exclusivamente via DataFrames — sem estado
global compartilhado.

## Tecnologias

- **Python 3.11**
- **pandas** — manipulação e transformação de dados
- **matplotlib / seaborn** — visualização
- **pytest** — testes unitários
- **GitHub Actions** — CI (testes automáticos em cada PR)
- **Git Flow** — develop / feature branches / main

## Como rodar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/tesouro-direto-eda.git
cd tesouro-direto-eda

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

Baixe o CSV consolidado em [Tesouro Transparente](https://www.tesourotransparente.gov.br/ckan/dataset/taxas-dos-titulos-ofertados-pelo-tesouro-direto)
e salve em `data/raw/PrecoTaxaTesouroDireto.csv`.

```bash
# Execute o pipeline completo
python main.py

# Rode os testes
python -m pytest tests/ -v
```

## Estrutura do projeto
tesouro-direto-eda/

├── .github/workflows/ci.yml   # Pipeline de CI

├── data/raw/                  # Dado bruto (não versionado)

├── src/

│   ├── config.py              # Constantes e paths centralizados

│   ├── ingestion.py           # Leitura do CSV bruto

│   ├── cleaning.py            # Limpeza e tipagem

│   ├── analysis.py            # Cálculos e agregações

│   ├── visualization.py       # Geração de gráficos

│   └── insights.py            # Interpretações de negócio

├── tests/                     # Testes unitários (pytest)

├── outputs/

│   ├── figures/                # Gráficos gerados (.png)

│   └── insights.md             # Relatório de insights

├── main.py                    # Entry point do pipeline

└── pytest.ini

## Insights encontrados

Resumo gerado automaticamente pelo pipeline — veja o relatório completo em
[`outputs/insights.md`](outputs/insights.md) após executar `python main.py`.

Exemplos do tipo de interpretação gerada:
- Identificação do título com maior/menor spread médio (custo implícito de negociação)
- Tendência de alta/queda nas taxas de cada título no período analisado
- Mês historicamente associado às maiores e menores taxas médias por título
