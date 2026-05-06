"""
cleaning.py — Responsável por limpar e padronizar os dados brutos.
Recebe o DataFrame cru e retorna um DataFrame pronto para análise.
"""

import pandas as pd


# Mapeamento dos nomes originais das colunas para nomes padronizados
COLUMN_MAPPING = {
    "Tipo Titulo": "tipo_titulo",
    "Data Vencimento": "data_vencimento",
    "Data Base": "data_base",
    "Taxa Compra Manha": "taxa_compra",
    "Taxa Venda Manha": "taxa_venda",
    "PU Compra Manha": "pu_compra",
    "PU Venda Manha": "pu_venda",
    "PU Base Manha": "pu_base",
}


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renomeia colunas para o padrão snake_case do projeto."""
    df = df.rename(columns=COLUMN_MAPPING)
    print(f"[cleaning] Colunas renomeadas: {list(df.columns)}")
    return df


def drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas onde as colunas essenciais são nulas."""
    essential_cols = ["tipo_titulo", "data_base", "taxa_compra", "taxa_venda"]
    before = len(df)
    df = df.dropna(subset=essential_cols)
    removed = before - len(df)
    print(f"[cleaning] Linhas removidas por valores nulos: {removed}")
    return df


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas para os tipos corretos."""
    df["data_base"] = pd.to_datetime(df["data_base"], dayfirst=True, errors="coerce")
    df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], dayfirst=True, errors="coerce")

    numeric_cols = ["taxa_compra", "taxa_venda", "pu_compra", "pu_venda", "pu_base"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    print("[cleaning] Tipos convertidos com sucesso")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas derivadas úteis para análise."""
    df["spread"] = df["taxa_compra"] - df["taxa_venda"]
    df["ano"] = df["data_base"].dt.year
    df["mes"] = df["data_base"].dt.month
    df["ano_mes"] = df["data_base"].dt.to_period("M")
    print("[cleaning] Colunas derivadas adicionadas: spread, ano, mes, ano_mes")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline completo de limpeza.
    Orquestra todas as etapas de limpeza em sequência.

    Args:
        df: DataFrame bruto vindo da ingestão.

    Returns:
        DataFrame limpo e pronto para análise.
    """
    print("[cleaning] Iniciando pipeline de limpeza...")
    df = rename_columns(df)
    df = drop_invalid_rows(df)
    df = convert_dtypes(df)
    df = add_derived_columns(df)
    df = df.reset_index(drop=True)
    print(f"[cleaning] Pipeline concluído. Shape final: {df.shape}")
    return df