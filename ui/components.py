"""
ui/components.py
================
Funciones de UI reutilizables que generan HTML o transforman datos
para visualización. No contienen llamadas directas a `st.*`.
"""

from typing import List, Tuple
from config import HC_COLOR, SA_COLOR, WIN_COLOR
from ui.icons import icon as _icon


def metric_card(
    icon_name: str,
    title: str,
    hc_val: str,
    sa_val: str,
    winner: str,
) -> str:
    """
    Genera el HTML de una tarjeta de métrica con badge al ganador.

    Args:
        icon_name: Clave de ícono Lucide (ver ui/icons.py).
        title:     Título de la métrica.
        hc_val:    Valor formateado de Hill Climbing.
        sa_val:    Valor formateado de Simulated Annealing.
        winner:    "hc", "sa" o "tie".

    Returns:
        String HTML listo para `st.markdown(..., unsafe_allow_html=True)`.
    """
    hc_col   = WIN_COLOR if winner == "hc" else HC_COLOR
    sa_col   = WIN_COLOR if winner == "sa" else SA_COLOR
    hc_badge = '<span class="badge-winner">GANADOR</span>' if winner == "hc" else ""
    sa_badge = '<span class="badge-winner">GANADOR</span>' if winner == "sa" else ""
    ico      = _icon(icon_name, size=13, color="#8892A4", style="margin-right:5px;")
    return f"""
    <div class="metric-card">
        <div class="metric-title">{ico}{title}</div>
        <div class="metric-row">
            <div class="metric-col">
                <div class="metric-label">Hill Climbing</div>
                <div class="metric-value" style="color:{hc_col}">
                    <span>{hc_val}</span>{hc_badge}
                </div>
            </div>
            <div class="metric-col">
                <div class="metric-label">Simulated Annealing</div>
                <div class="metric-value" style="color:{sa_col}">
                    <span>{sa_val}</span>{sa_badge}
                </div>
            </div>
        </div>
    </div>"""


def downsample(
    values: List[float],
    max_pts: int = 3000,
) -> Tuple[List[int], List[float]]:
    """
    Reduce el número de puntos de una serie conservando el primero y el último.

    Útil para graficar historiales de miles de iteraciones sin saturar Plotly.

    Args:
        values:  Lista de valores a muestrear.
        max_pts: Máximo de puntos en la salida.

    Returns:
        Tupla (índices, valores_muestreados).
    """
    n = len(values)
    if n <= max_pts:
        return list(range(n)), values
    step = n / max_pts
    idxs = sorted(set([int(i * step) for i in range(max_pts)] + [n - 1]))
    return idxs, [values[i] for i in idxs]