import pandas as pd


def get_taxa_evolution(df: pd.DataFrame, titulo: str) -> pd.DataFrame:
    """Retorna a série temporal de taxa_venda para um título, ordenada por data."""
    filtered = df.loc[df["tipo_titulo"] == titulo, ["data_base", "taxa_venda", "tipo_titulo"]]
    return filtered.dropna().sort_values("data_base")


def get_spread_medio(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna o spread médio (compra - venda) por título, do maior para o menor."""
    return (
        df.groupby("tipo_titulo")["spread"]
        .mean()
        .reset_index(name="spread_medio")
        .sort_values("spread_medio", ascending=False)
    )


def get_sazonalidade(df: pd.DataFrame, titulo: str) -> pd.DataFrame:
    """Retorna a taxa_venda média por mês do ano para um título específico."""
    filtered = df[df["tipo_titulo"] == titulo]
    return filtered.groupby("mes")["taxa_venda"].mean().reset_index(name="taxa_media")


def get_titulos_disponiveis(df: pd.DataFrame) -> list[str]:
    """Retorna a lista ordenada de títulos únicos presentes no dataset."""
    return sorted(df["tipo_titulo"].unique())