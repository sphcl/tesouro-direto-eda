from src.ingestion import load_raw_data
from src.cleaning import clean_data


def main():
    print("=" * 50)
    print("Pipeline Tesouro Direto EDA iniciado")
    print("=" * 50)

    # Etapa 1: Ingestão
    df_raw = load_raw_data()

    # Etapa 2: Limpeza
    df_clean = clean_data(df_raw)

    # Validação rápida
    print("\n--- Amostra dos dados limpos ---")
    print(df_clean.head())
    print("\n--- Tipos das colunas ---")
    print(df_clean.dtypes)
    print("\n--- Títulos únicos encontrados ---")
    print(df_clean["tipo_titulo"].unique())


if __name__ == "__main__":
    main()