"""Visualizações interativas com Plotly — exclusivas para o dashboard Streamlit."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MESES_PT = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def plot_taxa_evolution_plotly(df: pd.DataFrame, titulo: str, template: str) -> go.Figure:
    """Linha interativa da evolução de taxa de venda com hover e zoom."""
    fig = px.line(
        df,
        x="data_base",
        y="taxa_venda",
        title=f"Evolução da Taxa de Venda — {titulo}",
        labels={"data_base": "Data", "taxa_venda": "Taxa de Venda (% a.a.)"},
        template=template,
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(hovermode="x unified", title_font_size=15)
    return fig


def plot_spread_medio_plotly(df: pd.DataFrame, template: str) -> go.Figure:
    """Barras horizontais do spread médio por título."""
    fig = px.bar(
        df,
        x="spread_medio",
        y="tipo_titulo",
        orientation="h",
        title="Spread Médio por Título (Compra - Venda)",
        labels={"spread_medio": "Spread Médio (p.p.)", "tipo_titulo": ""},
        template=template,
        color="spread_medio",
        color_continuous_scale="Blues",
    )
    fig.update_layout(title_font_size=15, coloraxis_showscale=False)
    return fig


def plot_sazonalidade_plotly(df: pd.DataFrame, titulo: str, template: str) -> go.Figure:
    """Barras de sazonalidade mensal com nome dos meses em PT-BR."""
    df = df.copy()
    df["mes_nome"] = df["mes"].apply(lambda m: MESES_PT[m - 1])

    fig = px.bar(
        df,
        x="mes_nome",
        y="taxa_media",
        title=f"Sazonalidade da Taxa — {titulo}",
        labels={"mes_nome": "Mês", "taxa_media": "Taxa Média (% a.a.)"},
        template=template,
        color="taxa_media",
        color_continuous_scale="RdYlGn_r",
    )
    fig.update_layout(title_font_size=15, coloraxis_showscale=False)
    return fig


def plot_comparacao_plotly(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    titulo1: str,
    titulo2: str,
    template: str,
) -> go.Figure:
    """Linha dupla comparando a taxa de venda de dois títulos no mesmo gráfico."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df1["data_base"], y=df1["taxa_venda"],
        name=titulo1, line=dict(color="#2563eb", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=df2["data_base"], y=df2["taxa_venda"],
        name=titulo2, line=dict(color="#dc2626", width=2),
    ))

    fig.update_layout(
        title="Comparação de Taxas entre Títulos",
        title_font_size=15,
        xaxis_title="Data",
        yaxis_title="Taxa de Venda (% a.a.)",
        template=template,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig