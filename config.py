"""
config.py
=========
Constantes globales de la aplicación: paleta de colores y helper de layout Plotly.
Importar desde aquí en todos los demás módulos para evitar valores duplicados.
"""

# ── Paleta de colores ────────────────────────────────────────────────────────

DARK_BG    = "#0F1117"
SIDEBAR_BG = "#1A1D2E"
CARD_BG    = "#1E2130"
GRID_COLOR = "#2A2D3E"
HC_COLOR   = "#00B4D8"
SA_COLOR   = "#F4A261"
WIN_COLOR  = "#2A9D8F"


# ── Helper de layout Plotly ──────────────────────────────────────────────────

def dark_layout(title: str = "") -> dict:
    """Devuelve un dict de layout Plotly con tema oscuro consistente."""
    return dict(
        title=dict(text=title, font=dict(color="#E2E8F0", size=15)),
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color="#CBD5E0", family="sans-serif"),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=False),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, showline=False),
        legend=dict(
            bgcolor="rgba(30,33,48,0.85)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
        ),
        margin=dict(l=60, r=40, t=56, b=56),
    )