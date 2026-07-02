"""
Camada de serviço para consumo do pipeline por interfaces externas (dashboard/API).

Mantém os dados limpos em cache de processo para evitar reprocessar o CSV
a cada interação do usuário.
"""

from functools import lru_cache
from typing import Optional
from datetime import date

import pandas as pd

from src.ingestion import load_raw_data
from src.cleaning import clean_data
from src.analysis import (
    get_taxa_evolution,
    get_spread_medio,
    get_sazonalidade,
    get_titulos_disponiveis,
)


@lru_cache(maxsize=1)
def get_clean_dataset() -> pd.DataFrame:
    """Carrega e limpa o dataset uma única vez por processo, mantendo em cache."""
    return clean_data(load_raw_data())


def list_titulos() -> list[str]:
    """Lista os títulos disponíveis no dataset limpo."""
    return get_titulos_disponiveis(get_clean_dataset())


def taxa_evolution_for(
    titulo: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    """Retorna a evolução de taxa para um título, com filtro de período opcional."""
    df = get_taxa_evolution(get_clean_dataset(), titulo)
    if start_date is not None:
        df = df[df["data_base"] >= pd.Timestamp(start_date)]
    if end_date is not None:
        df = df[df["data_base"] <= pd.Timestamp(end_date)]
    return df


def spread_medio() -> pd.DataFrame:
    """Retorna o spread médio por título."""
    return get_spread_medio(get_clean_dataset())


def sazonalidade_for(titulo: str) -> pd.DataFrame:
    """Retorna a sazonalidade mensal para um título."""
    return get_sazonalidade(get_clean_dataset(), titulo)