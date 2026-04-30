"""
sections/convergence.py
=======================
Renderiza la Sección 2: gráfico de convergencia de la solución.
"""

from typing import Any, Dict

import streamlit as st

from charts import build_convergence_chart
from config import CARD_BG, HC_COLOR, SA_COLOR


def render(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    winner_val: str,
) -> None:
    """
    Muestra el expander explicativo y la figura de convergencia.

    Args:
        result_hc:  Resultado completo de Hill Climbing.
        result_sa:  Resultado completo de Simulated Annealing.
        winner_val: "hc", "sa" o "tie".
    """
    st.subheader("📉 Convergencia de la Solución")

    st.markdown(
        f"""
<div style="background:{CARD_BG}; border-radius:10px; padding:14px 20px;
            border-left:3px solid {HC_COLOR}; margin-bottom:2rem;">
  <span style="color:#E2E8F0; font-size:14px; line-height:1.7;">
    <b style="color:{HC_COLOR}">HC</b> converge rápido pero queda atrapado en un óptimo local
    (línea azul se aplana y el algoritmo se detiene).
    <b style="color:{SA_COLOR}">SA</b> acepta soluciones peores temporalmente
    <b style="color:{SA_COLOR}">(zona naranja)</b> para escapar y seguir buscando algo mejor.
    <br><b>↓ Cada bajada en la línea = nueva mejor solución encontrada.</b>
  </span>
</div>
""",
        unsafe_allow_html=True,
    )

    fig = build_convergence_chart(result_hc, result_sa, winner_val)
    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)