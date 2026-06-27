import logging
from pathlib import Path

from src.ingestion import load_raw_data
from src.cleaning import clean_data
from src.analysis import (
    get_taxa_evolution,
    get_spread_medio,
    get_sazonalidade,
    get_titulos_disponiveis,
)
from src.visualization import (
    plot_taxa_evolution,
    plot_spread_medio,
    plot_sazonalidade,
)

from src.insights import build_spread_insight, build_taxa_trend_insight, build_sazonalidade_insight

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_pipeline() -> None:
    df = clean_data(load_raw_data())
    titulos = get_titulos_disponiveis(df)
    logger.info("Títulos disponíveis: %s", titulos)

    insights = ["# Insights — Tesouro Direto\n"]

    for titulo in titulos:
        df_taxa = get_taxa_evolution(df, titulo)
        if not df_taxa.empty:
            plot_taxa_evolution(df_taxa, titulo)
            insights.append(build_taxa_trend_insight(df_taxa, titulo))

        df_saz = get_sazonalidade(df, titulo)
        if not df_saz.empty:
            plot_sazonalidade(df_saz, titulo)
            insights.append(build_sazonalidade_insight(df_saz, titulo))

    df_spread = get_spread_medio(df)
    plot_spread_medio(df_spread)
    insights.append(build_spread_insight(df_spread))

    Path("outputs/insights.md").write_text("\n\n".join(insights), encoding="utf-8")
    logger.info("Insights salvos em outputs/insights.md")
    logger.info("Pipeline concluído. Gráficos salvos em outputs/figures/")

if __name__ == "__main__":
    run_pipeline()