"""
ui/styles.py
============
CSS global de la aplicación.
Llamar a `inject()` una sola vez al inicio de app.py.
"""

import streamlit as st
from config import (
    CARD_BG, DARK_BG, GRID_COLOR, SA_COLOR, SIDEBAR_BG, WIN_COLOR
)


def inject() -> None:
    """Inyecta el CSS personalizado en la aplicación Streamlit."""
    st.markdown(
        f"""
<style>
/* ── Fondo principal ── */
.stApp {{
    background-color: {DARK_BG};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
    border-right: 1px solid {GRID_COLOR};
}}
[data-testid="stSidebar"] * {{
    color: #CBD5E0;
}}

/* ── Tarjetas de métricas ── */
.metric-card {{
    background-color: {CARD_BG};
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.45);
    margin-bottom: 8px;
    border: 1px solid {GRID_COLOR};
    /* sin height fijo: crece con el contenido */
    min-height: 130px;
    box-sizing: border-box;
}}
.metric-title {{
    color: #8892A4;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
}}
.metric-row {{
    display: flex;
    flex-direction: column;   /* HC arriba, SA abajo — sin superposición */
    gap: 12px;
}}
.metric-col {{
    display: flex;
    flex-direction: column;
    gap: 2px;
}}
.metric-label {{
    color: #8892A4;
    font-size: 10px;
    margin-bottom: 3px;
}}
.metric-value {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.02em;
    /* permitir wrap si el badge no cabe en una línea */
    white-space: normal;
    word-break: break-word;
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}}
.badge-winner {{
    display: inline-block;
    background-color: {WIN_COLOR};
    color: #fff;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.04em;
    white-space: nowrap;
    flex-shrink: 0;
}}

/* ── Tarjeta de conclusión ── */
.conclusion-card {{
    background: linear-gradient(135deg, {CARD_BG} 0%, #252A3D 100%);
    border-radius: 16px;
    padding: 28px 32px;
    border-left: 4px solid {WIN_COLOR};
    box-shadow: 0 8px 28px rgba(0,0,0,0.45);
    margin-top: 8px;
}}

/* ── Mejoras generales ── */
h1, h2, h3 {{ color: #E2E8F0 !important; }}
p, li {{ color: #CBD5E0; }}
.stDataFrame {{ border-radius: 8px; overflow: hidden; }}

/* ── Barra de progreso color SA ── */
.stProgress > div > div > div > div {{
    background-color: {SA_COLOR};
}}
</style>
""",
        unsafe_allow_html=True,
    )