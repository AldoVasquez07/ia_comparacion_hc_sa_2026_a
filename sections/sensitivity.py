"""
sections/sensitivity.py
=======================
Renderiza la Sección 5: análisis de sensibilidad de hiperparámetros de SA.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from config import CARD_BG, SA_COLOR, HC_COLOR, WIN_COLOR, dark_layout
from runners import run_sa


def render(prob_name: str, n_used: int, seed_used: int) -> None:
    """
    Expander con análisis de sensibilidad de T₀ y cooling rate.

    Args:
        prob_name: "misti" o "tsp".
        n_used:    N del experimento actual.
        seed_used: Semilla del experimento actual.
    """
    with st.expander("📊 Análisis de Sensibilidad de Hiperparámetros", expanded=False):
        st.markdown(
            "Compara cómo la **temperatura inicial** y el **cooling rate** "
            "afectan la calidad de la solución de SA."
        )

        if st.button("🔬 Ejecutar Análisis de Sensibilidad", key="run_hyp"):
            st.session_state["hyperparam_done"] = True

        if not st.session_state.get("hyperparam_done"):
            return

        temps  = [10.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
        crates = [0.950, 0.970, 0.990, 0.995, 0.999]

        with st.spinner("Ejecutando análisis de sensibilidad (resultados cacheados)..."):
            vals_temp = [
                run_sa(prob_name, n_used, seed_used, t, 0.995, 0.001)["best_value"]
                for t in temps
            ]
            vals_cr = [
                run_sa(prob_name, n_used, seed_used, 500.0, cr, 0.001)["best_value"]
                for cr in crates
            ]

        best_t_idx  = int(np.argmin(vals_temp))
        best_cr_idx = int(np.argmin(vals_cr))

        col1, col2 = st.columns(2)

        with col1:
            fig_t = go.Figure()
            fig_t.add_trace(go.Scatter(
                x=temps, y=vals_temp,
                mode="lines+markers",
                line=dict(color=SA_COLOR, width=3),
                marker=dict(size=10, color=SA_COLOR, line=dict(width=1.5, color="white")),
                hovertemplate="T₀=%{x:.0f}<br>Valor=%{y:.5f}<extra></extra>",
            ))
            fig_t.add_annotation(
                x=temps[best_t_idx], y=vals_temp[best_t_idx],
                text=f"★ Mejor: T₀={temps[best_t_idx]:.0f}",
                arrowhead=2, arrowcolor=WIN_COLOR, arrowwidth=2,
                font=dict(color=WIN_COLOR, size=12),
                bgcolor=CARD_BG, bordercolor=WIN_COLOR, borderpad=5, ay=-40,
            )
            layout_t = dark_layout("Temperatura inicial vs Mejor valor")
            layout_t["xaxis"]["title"] = "Temperatura inicial (T₀)"
            layout_t["yaxis"]["title"] = "Mejor valor encontrado"
            fig_t.update_layout(**layout_t)
            st.plotly_chart(fig_t, use_container_width=True, key="plot_temps")

        with col2:
            fig_cr = go.Figure()
            fig_cr.add_trace(go.Scatter(
                x=crates, y=vals_cr,
                mode="lines+markers",
                line=dict(color=HC_COLOR, width=3),
                marker=dict(size=10, color=HC_COLOR, line=dict(width=1.5, color="white")),
                hovertemplate="α=%{x:.3f}<br>Valor=%{y:.5f}<extra></extra>",
            ))
            fig_cr.add_annotation(
                x=crates[best_cr_idx], y=vals_cr[best_cr_idx],
                text=f"★ Mejor: α={crates[best_cr_idx]:.3f}",
                arrowhead=2, arrowcolor=WIN_COLOR, arrowwidth=2,
                font=dict(color=WIN_COLOR, size=12),
                bgcolor=CARD_BG, bordercolor=WIN_COLOR, borderpad=5, ay=-40,
            )
            layout_cr = dark_layout("Cooling rate vs Mejor valor")
            layout_cr["xaxis"]["title"] = "Cooling rate (α)"
            layout_cr["yaxis"]["title"] = "Mejor valor encontrado"
            fig_cr.update_layout(**layout_cr)
            st.plotly_chart(fig_cr, use_container_width=True, key="plot_cr")

        st.info(
            "💾 Cada gráfico de Plotly incluye el botón de **descarga PNG** "
            "(ícono 📷 en la barra superior del gráfico al pasar el cursor)."
        )