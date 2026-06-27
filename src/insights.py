import pandas as pd


def build_spread_insight(df_spread: pd.DataFrame) -> str:
    """Gera interpretação textual sobre o spread médio por título."""
    maior = df_spread.iloc[0]
    menor = df_spread.iloc[-1]

    return (
        f"O título com maior spread médio é **{maior['tipo_titulo']}** "
        f"({maior['spread_medio']:.2f} p.p.), indicando maior custo implícito "
        f"para quem compra e vende no mesmo dia. Já **{menor['tipo_titulo']}** "
        f"apresenta o menor spread ({menor['spread_medio']:.2f} p.p.), sugerindo "
        f"maior liquidez e eficiência de precificação."
    )


def build_taxa_trend_insight(df_taxa: pd.DataFrame, titulo: str) -> str:
    """Gera interpretação sobre a tendência da taxa de um título ao longo do tempo."""
    primeira = df_taxa.iloc[0]["taxa_venda"]
    ultima = df_taxa.iloc[-1]["taxa_venda"]
    variacao = ultima - primeira
    direcao = "alta" if variacao > 0 else "queda"

    return (
        f"A taxa de **{titulo}** variou de {primeira:.2f}% para {ultima:.2f}% "
        f"no período analisado — uma {direcao} de {abs(variacao):.2f} p.p., "
        f"refletindo o ciclo de política monetária vigente em cada momento."
    )


def build_sazonalidade_insight(df_saz: pd.DataFrame, titulo: str) -> str:
    """Gera interpretação sobre o mês de maior e menor taxa média."""
    mes_maior = df_saz.loc[df_saz["taxa_media"].idxmax()]
    mes_menor = df_saz.loc[df_saz["taxa_media"].idxmin()]

    return (
        f"Para **{titulo}**, o mês {int(mes_maior['mes'])} historicamente "
        f"apresenta a maior taxa média ({mes_maior['taxa_media']:.2f}%), "
        f"enquanto o mês {int(mes_menor['mes'])} apresenta a menor "
        f"({mes_menor['taxa_media']:.2f}%)."
    )