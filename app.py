import pandas as pd
import streamlit as st

from pathlib import Path
from src.data_service import (
    get_clean_dataset,
    list_titulos,
    spread_medio,
    sazonalidade_for,
    taxa_evolution_for,
)
from src.insights import (
    build_sazonalidade_insight,
    build_spread_insight,
    build_taxa_trend_insight,
)
from src.visualization_plotly import (
    plot_comparacao_plotly,
    plot_sazonalidade_plotly,
    plot_spread_medio_plotly,
    plot_taxa_evolution_plotly,
)

def inject_theme(dark: bool) -> None:
    theme = "dark" if dark else "light"
    css = Path(f"assets/{theme}.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Tesouro Direto — EDA",
    page_icon="📊",
    layout="wide",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def get_template() -> str:
    return "plotly_dark" if st.session_state.dark_mode else "plotly_white"


def render_sidebar() -> tuple:
    st.sidebar.title("Tesouro Direto EDA")
    st.sidebar.markdown("Análise exploratória de taxas e preços dos títulos públicos.")
    st.sidebar.markdown("---")

    titulos = list_titulos()
    titulo = st.sidebar.selectbox("Título principal", titulos)

    comparar = st.sidebar.checkbox("Comparar com outro título")
    titulo2 = None
    if comparar:
        outros = [t for t in titulos if t != titulo]
        titulo2 = st.sidebar.selectbox("Segundo título", outros)

    st.sidebar.markdown("---")

    df = get_clean_dataset()
    min_date = df["data_base"].min().date()
    max_date = df["data_base"].max().date()

    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    start_date = date_range[0] if len(date_range) > 0 else min_date
    end_date = date_range[1] if len(date_range) > 1 else max_date

    st.sidebar.markdown("---")
    st.sidebar.caption("Fonte: Tesouro Transparente")

    return titulo, titulo2, start_date, end_date


def render_kpis(titulo: str, start_date, end_date) -> None:
    """Renderiza os cards de métricas no topo do dashboard."""
    df = get_clean_dataset()
    df_filtrado = df[
        (df["tipo_titulo"] == titulo) &
        (df["data_base"] >= pd.Timestamp(start_date)) &
        (df["data_base"] <= pd.Timestamp(end_date))
    ]

    taxa_atual = (
        df_filtrado.sort_values("data_base").iloc[-1]["taxa_venda"]
        if not df_filtrado.empty else 0.0
    )
    spread_med = df_filtrado["spread"].mean() if not df_filtrado.empty else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros no período", f"{len(df_filtrado):,}".replace(",", "."))
    col2.metric("Taxa atual (% a.a.)", f"{taxa_atual:.2f}%")
    col3.metric("Spread médio", f"{spread_med:.2f} p.p.")
    col4.metric("Títulos disponíveis", len(list_titulos()))


def render_taxa_evolution(titulo: str, start_date, end_date) -> None:
    st.subheader("Evolução da Taxa de Venda")
    df = taxa_evolution_for(titulo, start_date, end_date)

    if df.empty:
        st.warning(f"Sem dados para {titulo} no período selecionado.")
        return

    st.plotly_chart(
        plot_taxa_evolution_plotly(df, titulo, get_template()),
        use_container_width=True,
    )
    st.info(build_taxa_trend_insight(df, titulo))


def render_sazonalidade(titulo: str) -> None:
    st.subheader("Sazonalidade Mensal")
    df = sazonalidade_for(titulo)

    if df.empty:
        st.warning(f"Sem dados de sazonalidade para {titulo}.")
        return

    st.plotly_chart(
        plot_sazonalidade_plotly(df, titulo, get_template()),
        use_container_width=True,
    )
    st.info(build_sazonalidade_insight(df, titulo))


def render_comparacao(titulo1: str, titulo2: str, start_date, end_date) -> None:
    st.subheader("Comparação entre Títulos")
    df1 = taxa_evolution_for(titulo1, start_date, end_date)
    df2 = taxa_evolution_for(titulo2, start_date, end_date)

    if df1.empty or df2.empty:
        st.warning("Sem dados suficientes para comparação no período selecionado.")
        return

    st.plotly_chart(
        plot_comparacao_plotly(df1, df2, titulo1, titulo2, get_template()),
        use_container_width=True,
    )


def render_spread() -> None:
    st.subheader("Spread Médio por Título")
    df = spread_medio()
    st.plotly_chart(
        plot_spread_medio_plotly(df, get_template()),
        use_container_width=True,
    )
    st.info(build_spread_insight(df))


def main() -> None:
    dark = st.session_state.dark_mode
    inject_theme(dark)

    titulo, titulo2, start_date, end_date = render_sidebar()

    # Título + toggle no canto superior direito
    col_title, col_toggle = st.columns([11, 1])
    with col_title:
        st.title("📊 Análise Exploratória — Tesouro Direto")
    with col_toggle:
        st.markdown("<div style='padding-top: 18px'>", unsafe_allow_html=True)
        icon = "☀️" if dark else "🌙"
        if st.button(icon, key="theme_toggle"):
            st.session_state.dark_mode = not dark
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"Exibindo: **{titulo}** · Período: `{start_date}` → `{end_date}`")
    st.markdown("---")

    render_kpis(titulo, start_date, end_date)
    st.markdown("---")

    if titulo2:
        render_comparacao(titulo, titulo2, start_date, end_date)
        st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        render_taxa_evolution(titulo, start_date, end_date)
    with col2:
        render_sazonalidade(titulo)

    st.markdown("---")
    render_spread()


if __name__ == "__main__":
    main()