import logging
from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH

logger = logging.getLogger(__name__)


def load_raw_data(filepath: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Lê o CSV do Tesouro Direto e retorna um DataFrame bruto, sem transformações.

    Raises:
        FileNotFoundError: se o arquivo não existir no caminho informado.
    """
    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}. Baixe em: "
            "https://www.tesourotransparente.gov.br/ckan/dataset/"
            "taxas-dos-titulos-ofertados-pelo-tesouro-direto"
        )

    logger.info("Carregando dados de %s", filepath)

    df = pd.read_csv(filepath, sep=";", decimal=",", encoding="latin-1", dayfirst=True)

    logger.info("Dados carregados: %d linhas, %d colunas", *df.shape)
    return df