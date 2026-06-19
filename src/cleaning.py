import logging

import pandas as pd

from src.config import COLUMN_MAPPING, ESSENTIAL_COLUMNS

logger = logging.getLogger(__name__)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia colunas para snake_case conforme COLUMN_MAPPING."""
    return df.rename(columns=COLUMN_MAPPING)


def drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas com valores nulos em colunas essenciais."""
    before = len(df)
    df = df.dropna(subset=ESSENTIAL_COLUMNS)
    logger.info("Linhas removidas por valores nulos: %d", before - len(df))
    return df


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas de data e numéricas para os tipos corretos."""
    df["data_base"] = pd.to_datetime(df["data_base"], dayfirst=True, errors="coerce")
    df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], dayfirst=True, errors="coerce")

    numeric_cols = ["taxa_compra", "taxa_venda", "pu_compra", "pu_venda", "pu_base"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas derivadas: spread, ano, mês e ano_mes."""
    df["spread"] = df["taxa_compra"] - df["taxa_venda"]
    df["ano"] = df["data_base"].dt.year
    df["mes"] = df["data_base"].dt.month
    df["ano_mes"] = df["data_base"].dt.to_period("M")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Executa o pipeline completo de limpeza sobre o DataFrame bruto."""
    logger.info("Iniciando pipeline de limpeza")

    df = rename_columns(df)
    df = drop_invalid_rows(df)
    df = convert_dtypes(df)
    df = add_derived_columns(df)
    df = df.reset_index(drop=True)

    logger.info("Pipeline de limpeza concluído. Shape final: %s", df.shape)
    return df