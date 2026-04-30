"""
sections/comparison.py
======================
Renderiza la Sección 3: comparativa directa HC vs SA (barras dobles).
"""

from typing import Any, Dict

import streamlit as st

from charts import build_comparison_chart


def render(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    winner_val: str,
    winner_time: str,
    sa_is_better: bool,
    diff_pct: float,
    speed_ratio: float,
) -> None:
    """
    Muestra el resumen textual y la figura de barras comparativa.
    """
    hc_best  = result_hc["best_value"]
    sa_best  = result_sa["best_value"]
    hc_time  = result_hc["time_ms"]
    sa_time  = result_sa["time_ms"]

    st.subheader("⚖️ Comparativa Directa")

    # Resumen dinámico
    if sa_is_better:
        summary = (
            f"SA encontró una solución **{diff_pct:.1f}% MEJOR** que HC, "
            f"tardando **{speed_ratio:.1f}x más tiempo**."
        )
    elif diff_pct < 0.01:
        summary = (
            f"HC y SA encontraron la **misma calidad** de solución. "
            f"HC fue **{speed_ratio:.1f}x más rápido**."
        )
    else:
        summary = (
            f"HC encontró una solución **{diff_pct:.1f}% MEJOR** que SA "
            f"y fue **{speed_ratio:.1f}x más rápido**."
        )
    st.markdown(
        f"<p style='font-size:16px; color:#E2E8F0; margin-bottom:12px;'>{summary}</p>",
        unsafe_allow_html=True,
    )

    fig = build_comparison_chart(
        hc_time, sa_time, hc_best, sa_best,
        winner_time, winner_val, diff_pct, sa_is_better,
    )
    st.plotly_chart(fig, use_container_width=True)