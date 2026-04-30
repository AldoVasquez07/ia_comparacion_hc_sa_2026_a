"""
sections/scale.py
=================
Renderiza la Sección 7: tabla comparativa SA vs HC para TSP con N creciente.
"""

import pandas as pd
import streamlit as st

from runners import run_hc, run_sa


_NS = [10, 20, 50, 100]


def render(seed_used: int, initial_temp: float, cooling_rate: float) -> None:
    """
    Muestra la tabla de comparación TSP para N = 10, 20, 50, 100.

    Args:
        seed_used:    Semilla del experimento actual.
        initial_temp: T₀ del experimento actual.
        cooling_rate: α del experimento actual.
    """
    st.subheader("📊 SA vs HC a escala — TSP con N creciente")
    st.markdown(
        "<p style='color:#8892A4; font-size:13px; margin-top:-8px; margin-bottom:12px;'>"
        "Problema TSP con ciudades aleatorias — muestra cómo la ventaja de SA crece con N.</p>",
        unsafe_allow_html=True,
    )

    with st.spinner("Calculando tabla comparativa (resultados cacheados)..."):
        rows = []
        for nn in _NS:
            r_hc = run_hc("tsp", nn, seed_used)
            r_sa = run_sa("tsp", nn, seed_used, initial_temp, cooling_rate, 0.001)
            hc_v, sa_v = r_hc["best_value"], r_sa["best_value"]
            hc_t, sa_t = r_hc["time_ms"],    r_sa["time_ms"]
            diff = abs(hc_v - sa_v) / max(abs(hc_v), 1e-9) * 100.0
            rows.append({
                "N ciudades":      nn,
                "HC Distancia":    f"✓ {hc_v:.2f}" if hc_v <= sa_v else f"  {hc_v:.2f}",
                "SA Distancia":    f"✓ {sa_v:.2f}" if sa_v <  hc_v else f"  {sa_v:.2f}",
                "Diferencia (%)":  f"{diff:.1f}%",
                "HC Tiempo (ms)":  f"{hc_t:.1f}",
                "SA Tiempo (ms)":  f"{sa_t:.1f}",
                "Ganador Calidad": "SA 🟠" if sa_v < hc_v else ("HC 🔵" if hc_v < sa_v else "Empate"),
            })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption(
        "✓ indica el mejor valor en cada fila. "
        "Con N pequeño HC es suficiente. Con N grande (50+), SA supera claramente a HC "
        "escapando óptimos locales."
    )