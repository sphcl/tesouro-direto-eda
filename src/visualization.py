import logging

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import OUTPUT_DIR

logger = logging.getLogger(__name__)

sns.set_theme(style="whitegrid", palette="muted")
FIGSIZE_DEFAULT = (12, 5)
MESES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def _slugify(titulo: str) -> str:
    """Converte o nome do título em um slug seguro para nome de arquivo."""
    return titulo.lower().replace(" ", "_")


def _save_figure(fig: plt.Figure, filename: str) -> None:
    """Salva a figura no disco em outputs/figures/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    logger.info("Gráfico salvo em %s", filepath)


def plot_taxa_evolution(df: pd.DataFrame, titulo: str) -> plt.Figure:
    """Plota a evolução da taxa de venda ao longo do tempo. Retorna a figura."""
    fig, ax = plt.subplots(figsize=FIGSIZE_DEFAULT)

    ax.plot(df["data_base"], df["taxa_venda"], linewidth=1.5, color="#2563eb")
    ax.set_title(f"Evolução da Taxa de Venda — {titulo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Taxa de Venda (% a.a.)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate(rotation=45)

    _save_figure(fig, f"taxa_evolution_{_slugify(titulo)}.png")
    return fig


def plot_spread_medio(df: pd.DataFrame) -> plt.Figure:
    """Plota o spread médio por título em gráfico de barras horizontal. Retorna a figura."""
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(data=df, x="spread_medio", y="tipo_titulo", palette="Blues_d", ax=ax)
    ax.set_title("Spread Médio por Título (Compra - Venda)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Spread Médio (p.p.)")
    ax.set_ylabel("")

    _save_figure(fig, "spread_medio_por_titulo.png")
    return fig


def plot_sazonalidade(df: pd.DataFrame, titulo: str) -> plt.Figure:
    """Plota a taxa média por mês do ano. Retorna a figura."""
    fig, ax = plt.subplots(figsize=FIGSIZE_DEFAULT)

    sns.barplot(data=df, x="mes", y="taxa_media", palette="coolwarm", ax=ax)
    ax.set_title(f"Sazonalidade da Taxa — {titulo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Taxa Média (% a.a.)")
    ax.set_xticks(range(12))
    ax.set_xticklabels(MESES_PT)

    _save_figure(fig, f"sazonalidade_{_slugify(titulo)}.png")
    return fig