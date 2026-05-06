"""
ingestion.py — Responsável por carregar os dados brutos do Tesouro Direto.
Nenhuma transformação aqui. Apenas leitura e retorno do dado cru.
"""

import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/raw/tesouro_direto.xlsx")


def load_raw_data(filepath: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Lê o arquivo Excel do Tesouro Direto e retorna um DataFrame bruto.

    Args:
        filepath: Caminho para o arquivo .xlsx

    Returns:
        DataFrame com os dados brutos, sem nenhuma transformação.

    Raises:
        FileNotFoundError: Se o arquivo não existir no caminho informado.
    """
    if not filepath.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filepath}\n"
            "Baixe os dados em: https://www.tesourodireto.com.br/dados/historico-de-precos-e-taxas.htm"
        )

    print(f"[ingestion] Carregando dados de: {filepath}")

    df = pd.read_excel(
        filepath,
        sheet_name=0,
        header=1,        # O Excel do Tesouro tem uma linha de cabeçalho decorativo
        engine="openpyxl"
    )

    print(f"[ingestion] Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df