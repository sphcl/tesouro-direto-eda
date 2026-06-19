from pathlib import Path

RAW_DATA_PATH = Path("data/raw/PrecoTaxaTesouroDireto.csv")
OUTPUT_DIR = Path("outputs/figures")

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

ESSENTIAL_COLUMNS = ["tipo_titulo", "data_base", "taxa_compra", "taxa_venda"]