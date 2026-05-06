import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/PrecoTaxaTesouroDireto.csv")


def load_raw_data(filepath: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Lê o CSV do Tesouro Direto e retorna um DataFrame bruto.

    Args:
        filepath: Caminho para o arquivo .csv

    Returns:
        DataFrame com os dados brutos, sem nenhuma transformação.

    Raises:
        FileNotFoundError: Se o arquivo não existir no caminho informado.
    """
    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}\n"
            "Baixe os dados em: https://www.tesourotransparente.gov.br/ckan/dataset/"
            "taxas-dos-titulos-ofertados-pelo-tesouro-direto"
        )

    print(f"[ingestion] Carregando dados de: {filepath}")

    df = pd.read_csv(
        filepath,
        sep=";",
        decimal=",",
        encoding="latin-1",
        dayfirst=True,
    )

    print(f"[ingestion] Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df