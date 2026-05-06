"""
Testes unitários para o módulo de limpeza.
"""

import pandas as pd
import pytest
from src.cleaning import rename_columns, drop_invalid_rows, convert_dtypes, add_derived_columns


@pytest.fixture
def raw_df():
    """DataFrame simulando os dados brutos do Tesouro Direto."""
    return pd.DataFrame({
        "Tipo Titulo": ["Tesouro Selic 2029", "Tesouro IPCA+ 2035", None],
        "Data Vencimento": ["01/03/2029", "15/05/2035", "01/01/2030"],
        "Data Base": ["01/01/2023", "01/01/2023", None],
        "Taxa Compra Manha": [11.5, 6.2, 5.0],
        "Taxa Venda Manha": [11.4, 6.1, 4.9],
        "PU Compra Manha": [10000.0, 3500.0, 2000.0],
        "PU Venda Manha": [10010.0, 3510.0, 2010.0],
        "PU Base Manha": [10005.0, 3505.0, 2005.0],
    })


def test_rename_columns(raw_df):
    df = rename_columns(raw_df)
    assert "tipo_titulo" in df.columns
    assert "taxa_compra" in df.columns
    assert "data_base" in df.columns


def test_drop_invalid_rows(raw_df):
    df = rename_columns(raw_df)
    df = drop_invalid_rows(df)
    assert len(df) == 2


def test_convert_dtypes(raw_df):
    df = rename_columns(raw_df)
    df = drop_invalid_rows(df)
    df = convert_dtypes(df)
    assert pd.api.types.is_datetime64_any_dtype(df["data_base"])
    assert pd.api.types.is_float_dtype(df["taxa_compra"])


def test_add_derived_columns(raw_df):
    df = rename_columns(raw_df)
    df = drop_invalid_rows(df)
    df = convert_dtypes(df)
    df = add_derived_columns(df)
    assert "spread" in df.columns
    assert "ano" in df.columns
    assert "mes" in df.columns