"""
charts.py
=========
Funciones puras que construyen y devuelven figuras Plotly.
No dependen de `st.*`, lo que facilita pruebas unitarias independientes de Streamlit.
"""

from typing import Any, Dict, List

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import CARD_BG, DARK_BG, GRID_COLOR, HC_COLOR, SA_COLOR, WIN_COLOR, dark_layout
from ui.components import downsample


# ── Gráfico de convergencia ──────────────────────────────────────────────────

def build_convergence_chart(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    winner_val: str,
) -> go.Figure:
    """
    Construye la figura de evolución de la solución óptima por iteración.

    Args:
        result_hc:  Resultado completo de Hill Climbing.
        result_sa:  Resultado completo de Simulated Annealing.
        winner_val: "hc", "sa" o "tie".

    Returns:
        Figura Plotly lista para `st.plotly_chart`.
    """
    hc_idxs, hc_vals = downsample(result_hc["history"])
    sa_idxs, sa_vals = downsample(result_sa["history"])
    sa_max_x   = result_sa["iterations"]
    hc_conv_at = result_hc.get("converged_at", 0)

    fig = go.Figure()

    # Área y línea HC
    fig.add_trace(go.Scatter(
        x=hc_idxs, y=hc_vals, mode="lines", name="Hill Climbing",
        line=dict(color=HC_COLOR, width=3),
        fill="tozeroy", fillcolor="rgba(0,180,216,0.10)",
        hovertemplate="Iter: %{x}<br>Valor: %{y:.5f}<extra>Hill Climbing</extra>",
    ))
    step_hc = max(1, len(hc_idxs) // 25)
    fig.add_trace(go.Scatter(
        x=hc_idxs[::step_hc], y=hc_vals[::step_hc], mode="markers",
        marker=dict(color=HC_COLOR, size=7, symbol="circle",
                    line=dict(color="white", width=1)),
        showlegend=False, hoverinfo="skip",
    ))

    # Área y línea SA
    fig.add_trace(go.Scatter(
        x=sa_idxs, y=sa_vals, mode="lines", name="Simulated Annealing",
        line=dict(color=SA_COLOR, width=3),
        fill="tozeroy", fillcolor="rgba(244,162,97,0.10)",
        hovertemplate="Iter: %{x}<br>Valor: %{y:.5f}<extra>Simulated Annealing</extra>",
    ))
    step_sa = max(1, len(sa_idxs) // 25)
    fig.add_trace(go.Scatter(
        x=sa_idxs[::step_sa], y=sa_vals[::step_sa], mode="markers",
        marker=dict(color=SA_COLOR, size=7, symbol="circle",
                    line=dict(color="white", width=1)),
        showlegend=False, hoverinfo="skip",
    ))

    # Zona donde SA sigue explorando después de que HC se detuvo
    if hc_conv_at < sa_max_x:
        fig.add_vrect(
            x0=hc_conv_at, x1=sa_max_x,
            fillcolor="rgba(244,162,97,0.07)", line_width=0,
        )
        fig.add_annotation(
            x=(hc_conv_at + sa_max_x) / 2, y=0.92,
            xref="x", yref="paper",
            text=f"<b style='color:{SA_COLOR}'>SA sigue explorando →</b>",
            showarrow=False,
            font=dict(color=SA_COLOR, size=12),
            bgcolor="rgba(30,33,48,0.85)",
            bordercolor=SA_COLOR, borderwidth=1, borderpad=5,
        )

    # Línea vertical donde HC quedó atrapado
    fig.add_vline(
        x=hc_conv_at, line_dash="dash", line_color=HC_COLOR, line_width=2,
        annotation_text="   HC se queda atrapado aquí",
        annotation_position="top left",
        annotation_font=dict(color=HC_COLOR, size=11),
        annotation_bgcolor=CARD_BG,
        annotation_bordercolor=HC_COLOR,
        annotation_borderpad=5,
    )

    # Badge del ganador
    w_label = "Hill Climbing" if winner_val == "hc" else "Simulated Annealing"
    w_color = HC_COLOR if winner_val == "hc" else SA_COLOR
    fig.add_annotation(
        x=0.99, y=0.06, xref="paper", yref="paper",
        text=f"🏆 Ganador: {w_label}", showarrow=False,
        font=dict(color=w_color, size=12),
        bgcolor=CARD_BG, bordercolor=w_color, borderwidth=1, borderpad=6,
        align="right",
    )

    # Rango Y
    init_val = result_hc["history"][0]
    min_val  = min(min(hc_vals), min(sa_vals))
    spread   = max(init_val - min_val, init_val * 0.04)

    layout = dark_layout("Evolución de la Solución Óptima por Iteración")
    layout["xaxis"]["title"] = "Iteración"
    layout["yaxis"]["title"] = "Costo total — MENOR ES MEJOR ↓"
    layout["yaxis"]["range"] = [min_val - spread * 0.12, init_val + spread * 0.30]

    # Línea base (sin algoritmo)
    fig.add_hline(
        y=init_val, line_dash="dash", line_color="#FF4444", line_width=2.5,
        annotation_text="  ❌ Sin algoritmo (aleatorio)",
        annotation_position="top right",
        annotation_font=dict(color="#FF4444", size=11),
        annotation_bgcolor=CARD_BG, annotation_borderpad=4,
    )
    # Zona óptima
    fig.add_hrect(
        y0=min_val - spread * 0.12, y1=min_val,
        fillcolor="rgba(42,157,143,0.08)", line_width=0,
        annotation_text="Zona óptima 🎯",
        annotation_position="bottom right",
        annotation_font=dict(color=WIN_COLOR, size=10),
    )

    fig.update_layout(**layout)
    return fig


# ── Gráfico comparativo dual ─────────────────────────────────────────────────

def build_comparison_chart(
    hc_time: float,
    sa_time: float,
    hc_best: float,
    sa_best: float,
    winner_time: str,
    winner_val: str,
    diff_pct: float,
    sa_is_better: bool,
) -> go.Figure:
    """
    Construye el gráfico de barras doble (tiempo vs calidad).

    Returns:
        Figura Plotly lista para `st.plotly_chart`.
    """
    hc_qual_color = WIN_COLOR if winner_val == "hc" else HC_COLOR
    sa_qual_color = WIN_COLOR if winner_val == "sa" else SA_COLOR

    if sa_is_better:
        hc_qual_text = f"+{diff_pct:.1f}% peor\n{hc_best:.4f}"
        sa_qual_text = f"GANADOR ✓\n{sa_best:.4f}"
    elif diff_pct < 0.01:
        hc_qual_text = f"= empate\n{hc_best:.4f}"
        sa_qual_text = f"= empate\n{sa_best:.4f}"
    else:
        hc_qual_text = f"GANADOR ✓\n{hc_best:.4f}"
        sa_qual_text = f"+{diff_pct:.1f}% peor\n{sa_best:.4f}"

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "Tiempo de ejecución (ms)",
            "¿Quién encontró la mejor solución? (↓ menor = mejor)",
        ],
        horizontal_spacing=0.14,
    )

    # Barras de tiempo
    fig.add_trace(go.Bar(
        x=["Hill Climbing", "Simulated Annealing"],
        y=[hc_time, sa_time],
        marker_color=[
            WIN_COLOR if winner_time == "hc" else HC_COLOR,
            WIN_COLOR if winner_time == "sa" else SA_COLOR,
        ],
        text=[
            f"GANADOR ✓\n{hc_time:.1f} ms" if winner_time == "hc" else f"{hc_time:.1f} ms",
            f"GANADOR ✓\n{sa_time:.1f} ms" if winner_time == "sa" else f"{sa_time:.1f} ms",
        ],
        textposition="outside",
        textfont=dict(color="#CBD5E0", size=11),
        showlegend=False,
    ), row=1, col=1)

    # Barras de calidad
    fig.add_trace(go.Bar(
        x=["Hill Climbing", "Simulated Annealing"],
        y=[hc_best, sa_best],
        marker_color=[hc_qual_color, sa_qual_color],
        text=[hc_qual_text, sa_qual_text],
        textposition="outside",
        textfont=dict(color="#CBD5E0", size=11),
        showlegend=False,
    ), row=1, col=2)

    fig.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color="#CBD5E0", family="sans-serif"),
        margin=dict(l=40, r=40, t=70, b=40),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor=GRID_COLOR, showline=False)
    return fig


# ── Figuras de mapas / rutas ──────────────────────────────────────────────────

def build_tsp_figure(
    solution: List[int],
    cities: np.ndarray,
    title: str,
    line_col: str,
    cscale: str,
) -> go.Figure:
    """Genera la figura de ruta TSP con puntos coloreados por orden de visita."""
    n_c = len(solution)
    route_x, route_y = [], []
    for i in range(n_c):
        a, b = cities[solution[i]], cities[solution[(i + 1) % n_c]]
        route_x += [float(a[0]), float(b[0]), None]
        route_y += [float(a[1]), float(b[1]), None]

    pts_x = [float(cities[s][0]) for s in solution]
    pts_y = [float(cities[s][1]) for s in solution]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=route_x, y=route_y, mode="lines",
        line=dict(color=line_col, width=1.8, dash="dot"),
        showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=pts_x, y=pts_y, mode="markers+text",
        marker=dict(
            color=list(range(n_c)), colorscale=cscale, size=15,
            showscale=True,
            colorbar=dict(title="Orden en ruta", thickness=12),
            line=dict(width=1.5, color="white"),
        ),
        text=[str(i + 1) for i in range(n_c)],
        textposition="middle center",
        textfont=dict(color="white", size=8),
        hovertemplate="Ciudad %{text}<br>(%{x:.1f}, %{y:.1f})<extra></extra>",
        showlegend=False,
    ))

    dist = sum(
        float(np.sqrt(
            (cities[solution[i]][0] - cities[solution[(i + 1) % n_c]][0]) ** 2
            + (cities[solution[i]][1] - cities[solution[(i + 1) % n_c]][1]) ** 2
        ))
        for i in range(n_c)
    )
    fig.add_annotation(
        x=0.02, y=0.97, xref="paper", yref="paper",
        text=f"<b>Distancia total: {dist:.2f}</b>",
        showarrow=False, font=dict(color=line_col, size=13),
        bgcolor=CARD_BG, bordercolor=line_col, borderwidth=1, borderpad=7,
        align="left",
    )
    layout = dark_layout(title)
    layout["xaxis"]["title"] = "X"
    layout["yaxis"]["title"] = "Y"
    fig.update_layout(**layout)
    return fig


def build_misti_figure(
    solution: List[int],
    districts: list,
    dangers: np.ndarray,
    title: str,
    line_col: str,
) -> go.Figure:
    """
    Genera la figura del mapa de evacuación del Misti.
    Importa las coordenadas del volcán directamente desde el módulo del problema.
    """
    from problems.misti_evacuation import MISTI_LAT, MISTI_LON

    n_d   = len(solution)
    lats  = [d["lat"]  for d in districts]
    lons  = [d["lon"]  for d in districts]
    names = [d["name"] for d in districts]

    evac_order = [0] * n_d
    for rank, idx in enumerate(solution):
        evac_order[idx] = rank + 1

    dmin, dmax   = float(dangers.min()), float(dangers.max())
    danger_norm  = [
        (float(dangers[i]) - dmin) / max(dmax - dmin, 1e-9)
        for i in range(n_d)
    ]

    fig = go.Figure()

    # Líneas entre distritos en el orden de evacuación
    for step in range(n_d - 1):
        a_i, b_i = solution[step], solution[step + 1]
        fig.add_trace(go.Scatter(
            x=[lons[a_i], lons[b_i]], y=[lats[a_i], lats[b_i]],
            mode="lines",
            line=dict(color=line_col, width=1.6, dash="dot"),
            showlegend=False, hoverinfo="skip",
        ))

    # Distritos
    fig.add_trace(go.Scatter(
        x=lons, y=lats, mode="markers+text",
        marker=dict(
            color=danger_norm, colorscale="RdYlGn_r", size=22,
            showscale=True,
            colorbar=dict(
                title="Peligro", thickness=12,
                tickvals=[0.0, 1.0], ticktext=["Bajo", "Alto"],
            ),
            line=dict(width=1.5, color="white"),
        ),
        text=[str(evac_order[i]) for i in range(n_d)],
        textposition="middle center",
        textfont=dict(color="white", size=9, family="sans-serif"),
        customdata=[
            [names[i], f"{float(dangers[i]):.4f}", evac_order[i]]
            for i in range(n_d)
        ],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Peligro: %{customdata[1]}<br>"
            "Orden de evacuación: %{customdata[2]}<extra></extra>"
        ),
        showlegend=False,
    ))

    # Volcán Misti
    fig.add_trace(go.Scatter(
        x=[MISTI_LON], y=[MISTI_LAT], mode="markers+text",
        marker=dict(color="#FF4444", size=22, symbol="triangle-up",
                    line=dict(width=2, color="white")),
        text=["🌋 Misti"],
        textposition="top center",
        textfont=dict(color="#FF6666", size=11),
        showlegend=False,
        hovertemplate=(
            "<b>Volcán Misti</b><br>"
            "Lat: -16.294°<br>Lon: -71.409°<extra></extra>"
        ),
    ))

    layout = dark_layout(title)
    layout["xaxis"]["title"] = "Longitud"
    layout["yaxis"]["title"] = "Latitud"
    fig.update_layout(**layout)
    return fig