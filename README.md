# Análise Exploratória de Dados - Tesouro Direto

Projeto de análise exploratória de dados (EDA) sobre os títulos públicos
do Tesouro Direto, com foco em evolução de taxas, spread e sazonalidade.

## Status
Em desenvolvimento

## Tecnologias
- Python 3.x
- pandas
- matplotlib
- seaborn

## Como rodar

```bash
git clone https://github.com/seu-usuario/tesouro-direto-eda.git
cd tesouro-direto-eda

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Estrutura
```
tesouro-direto-eda/
├── data/           # Dados brutos e processados
├── src/            # Módulos Python
├── outputs/        # Gráficos gerados
└── main.py         # Entry point
```