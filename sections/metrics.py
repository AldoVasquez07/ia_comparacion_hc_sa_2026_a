"""
sections/metrics.py
===================
Renderiza las tarjetas de métricas (Sección 1) y el banner del ganador.
"""

from typing import Any, Dict

import streamlit as st

from config import CARD_BG, HC_COLOR, SA_COLOR, WIN_COLOR
from ui.components import metric_card
from ui.icons import icon as _icon


def render(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    winner_val: str,
    winner_time: str,
    winner_iters: str,
    winner_improv: str,
    sa_is_better: bool,
    diff_pct: float,
    speed_ratio: float,
    prob_display: str,
    n_used: int,
) -> None:
    """
    Muestra las 4 tarjetas de métricas y el banner resumen del ganador.

    Args:
        result_hc/sa: Resultados completos de cada algoritmo.
        winner_*:     "hc", "sa" o "tie" según cada métrica.
        sa_is_better: True si SA encontró mejor valor.
        diff_pct:     Diferencia porcentual entre los valores.
        speed_ratio:  sa_time / hc_time.
        prob_display: Nombre amigable del problema.
        n_used:       N con que se ejecutó el experimento.
    """
    hc_best  = result_hc["best_value"]
    sa_best  = result_sa["best_value"]
    hc_time  = result_hc["time_ms"]
    sa_time  = result_sa["time_ms"]
    hc_iters = result_hc["iterations"]
    sa_iters = result_sa["iterations"]
    hc_improv = result_hc["improvement_pct"]
    sa_improv = result_sa["improvement_pct"]

    st.subheader("📊 Resultados de la Comparación")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(metric_card(
            "target", "Mejor valor encontrado",
            f"{hc_best:.4f}", f"{sa_best:.4f}", winner_val,
        ), unsafe_allow_html=True)

    with c2:
        st.markdown(metric_card(
            "clock", "Tiempo de ejecución",
            f"{hc_time:.1f} ms", f"{sa_time:.1f} ms", winner_time,
        ), unsafe_allow_html=True)

    with c3:
        st.markdown(metric_card(
            "zap", "Iteraciones realizadas",
            f"{hc_iters:,}", f"{sa_iters:,}", winner_iters,
        ), unsafe_allow_html=True)

    with c4:
        st.markdown(metric_card(
            "trending-up", "Mejora sobre inicial",
            f"{hc_improv:.2f}%", f"{sa_improv:.2f}%", winner_improv,
        ), unsafe_allow_html=True)

    _render_winner_banner(
        sa_is_better, diff_pct, speed_ratio,
        hc_time, sa_time, prob_display, n_used,
    )


def _render_winner_banner(
    sa_is_better: bool,
    diff_pct: float,
    speed_ratio: float,
    hc_time: float,
    sa_time: float,
    prob_display: str,
    n_used: int,
) -> None:
    if sa_is_better:
        col, bg  = WIN_COLOR, "rgba(42,157,143,0.12)"
        ico      = _icon("award", size=18, color=WIN_COLOR, style="margin-right:8px;")
        head     = "SA GANÓ EN CALIDAD DE SOLUCIÓN"
        body     = (
            f"Simulated Annealing encontró una solución "
            f"<b>{diff_pct:.1f}% mejor</b> que Hill Climbing en {prob_display}."
        )
    elif diff_pct < 0.01:
        col, bg  = WIN_COLOR, "rgba(42,157,143,0.10)"
        ico      = _icon("check-circle", size=18, color=WIN_COLOR, style="margin-right:8px;")
        head     = "HC Y SA CONVERGIERON AL MISMO ÓPTIMO"
        body     = f"Ambos algoritmos encontraron la misma calidad de solución para N={n_used}."
    else:
        col, bg  = HC_COLOR, "rgba(0,180,216,0.10)"
        ico      = _icon("check-circle", size=18, color=HC_COLOR, style="margin-right:8px;")
        head     = f"HC FUE SUFICIENTE PARA N={n_used}"
        body     = (
            f"Hill Climbing encontró una solución "
            f"<b>{diff_pct:.1f}% mejor</b> que SA en este caso."
        )

    spd_ico = _icon("zap", size=14, color="#8892A4", style="margin-right:6px;")
    if speed_ratio > 1.1:
        speed_txt = (
            f"{spd_ico}HC fue <b>{speed_ratio:.1f}x más rápido</b> en tiempo de ejecución "
            f"({hc_time:.0f} ms vs {sa_time:.0f} ms)."
        )
    elif speed_ratio < 0.9:
        speed_txt = (
            f"{spd_ico}SA fue <b>{1/speed_ratio:.1f}x más rápido</b> "
            f"({sa_time:.0f} ms vs {hc_time:.0f} ms)."
        )
    else:
        speed_txt = f"{spd_ico}Ambos con tiempos similares ({hc_time:.0f} ms vs {sa_time:.0f} ms)."

    st.markdown(
        f"""
<div style="background:{bg}; border-radius:12px; padding:16px 22px;
            border-left:4px solid {col}; margin:8px 0 16px 0;">
  <div style="color:{col}; font-size:16px; font-weight:800; margin-bottom:6px;
              display:flex; align-items:center;">
    {ico}{head}
  </div>
  <p style="color:#CBD5E0; font-size:14px; margin:0 0 4px 0;">{body}</p>
  <p style="color:#8892A4; font-size:13px; margin:0; display:flex; align-items:center;">{speed_txt}</p>
</div>
""",
        unsafe_allow_html=True,
    )