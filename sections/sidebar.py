"""
sections/sidebar.py
===================
Renderiza el panel lateral completo y devuelve los parámetros seleccionados.
El caller (app.py) no necesita saber qué widgets existen en el sidebar.
"""

import math
from typing import Any, Dict, Tuple

import pandas as pd
import streamlit as st

from config import CARD_BG, GRID_COLOR, HC_COLOR, SA_COLOR, WIN_COLOR
from runners import run_hc, run_sa
from ui.icons import icon as _icon


def render() -> Tuple[str, str, int, int, float, float, bool]:
    """
    Renderiza el sidebar y devuelve los parámetros del experimento.

    Returns:
        (problem_name, problem_label, n, seed, initial_temp, cooling_rate, run_clicked)
    """
    with st.sidebar:
        ico_settings = _icon("settings",  size=15, color="#CBD5E0", style="margin-right:6px;vertical-align:-2px;")
        st.markdown(f"### {ico_settings} Configuración del Experimento", unsafe_allow_html=True)

        problem_label: str = st.selectbox(
            "Problema",
            ["Evacuación del Misti", "TSP - Viajero"],
        )
        problem_name: str = "misti" if "Misti" in problem_label else "tsp"

        if problem_name == "misti":
            n: int = st.slider("Número de distritos", min_value=3, max_value=10, value=10)
        else:
            n = st.slider("Número de ciudades", min_value=5, max_value=30, value=15)

        seed: int = st.slider("Semilla aleatoria", min_value=1, max_value=100, value=42)

        st.divider()
        ico_sliders = _icon("sliders", size=13, color="#CBD5E0", style="margin-right:5px;vertical-align:-1px;")
        st.markdown(f"#### {ico_sliders} Hiperparámetros SA", unsafe_allow_html=True)

        initial_temp: float = st.slider(
            "Temperatura inicial (T₀)",
            min_value=10.0, max_value=1000.0, value=500.0, step=10.0,
        )
        cooling_rate: float = st.slider(
            "Cooling rate (α)",
            min_value=0.900, max_value=0.999, value=0.995, step=0.001,
            format="%.3f",
        )
        min_temp: float = 0.001
        st.caption(f"Temperatura mínima fija: {min_temp}")

        if cooling_rate < 1.0 and initial_temp > min_temp:
            est_iters = int(math.log(min_temp / initial_temp) / math.log(cooling_rate))
            st.caption(f"Iteraciones SA estimadas: ~{est_iters:,}")

        st.divider()
        run_clicked: bool = st.button(
            "▶ Ejecutar Comparación", type="primary", use_container_width=True
        )

        _render_last_run_summary()
        _render_multi_n_comparison(problem_name, seed, initial_temp, cooling_rate, min_temp)
        _render_param_explainer()
        _render_presentation_button()

    return problem_name, problem_label, n, seed, initial_temp, cooling_rate, run_clicked


# ── Helpers internos del sidebar ─────────────────────────────────────────────

def _render_last_run_summary() -> None:
    """Muestra el resumen de la última ejecución si existe en session_state."""
    if "result_hc" not in st.session_state:
        return

    hc_v  = st.session_state["result_hc"]["best_value"]
    sa_v  = st.session_state["result_sa"]["best_value"]
    hc_t  = st.session_state["result_hc"]["time_ms"]
    sa_t  = st.session_state["result_sa"]["time_ms"]
    n_run = st.session_state.get("n_used", "?")

    sa_wins  = sa_v < hc_v
    diff_pct = abs(sa_v - hc_v) / max(abs(hc_v), 1e-9) * 100.0
    qual_col = SA_COLOR if sa_wins else HC_COLOR
    qual_lbl = (
        f"SA ganó ({diff_pct:.1f}% mejor)" if sa_wins
        else (f"HC ganó ({diff_pct:.1f}% mejor)" if diff_pct >= 0.01 else "Empate")
    )
    spd_x   = sa_t / max(hc_t, 0.001)
    spd_lbl = (
        f"HC fue {spd_x:.1f}x más rápido" if hc_t <= sa_t
        else f"SA fue {1/max(spd_x, 0.001):.1f}x más rápido"
    )

    ico_run   = _icon("activity",  size=12, color="#8892A4", style="margin-right:4px;vertical-align:-1px;")
    ico_qual  = _icon("award",     size=12, color=qual_col,  style="margin-right:4px;vertical-align:-1px;")
    ico_speed = _icon("zap",       size=12, color=WIN_COLOR, style="margin-right:4px;vertical-align:-1px;")

    st.markdown(
        f"""<div style="background:{CARD_BG}; border-radius:8px; padding:10px 12px;
                margin-top:8px; border:1px solid {GRID_COLOR}; font-size:12px;">
          <div style="color:#8892A4; font-weight:700; margin-bottom:6px;">
            {ico_run} Última ejecución (N={n_run})
          </div>
          <div style="color:{qual_col}; font-weight:700; margin-bottom:3px;">
            {ico_qual} Calidad: {qual_lbl}
          </div>
          <div style="color:{WIN_COLOR}; font-weight:700;">
            {ico_speed} Velocidad: {spd_lbl}
          </div>
        </div>""",
        unsafe_allow_html=True,
    )


def _render_multi_n_comparison(
    problem_name: str,
    seed: int,
    initial_temp: float,
    cooling_rate: float,
    min_temp: float,
) -> None:
    """Botón y tabla de comparación para múltiples valores de N."""
    st.divider()
    candidate_ns = [3, 5, 7, 10] if problem_name == "misti" else [5, 10, 15, 20]

    if st.button(
        "Comparar múltiples N",
        help=f"Ejecuta HC y SA para N = {candidate_ns} con semilla y parámetros actuales",
        use_container_width=True,
    ):
        st.session_state["sb_n_cmp_done"] = True
        st.session_state["sb_n_cmp_prob"] = problem_name

    if (
        st.session_state.get("sb_n_cmp_done")
        and st.session_state.get("sb_n_cmp_prob") == problem_name
    ):
        rows = []
        for cn in candidate_ns:
            r_hc = run_hc(problem_name, cn, seed)
            r_sa = run_sa(problem_name, cn, seed, initial_temp, cooling_rate, min_temp)
            hcv, sav = r_hc["best_value"], r_sa["best_value"]
            rows.append({
                "N": cn,
                "HC": f"{hcv:.3f}",
                "SA": f"{sav:.3f}",
                "Ganador": "SA 🟠" if sav < hcv else "HC 🔵",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_param_explainer() -> None:
    """Expander con la explicación de cada parámetro."""
    with st.expander("Qué significa cada parámetro"):
        st.markdown("""
**Temperatura inicial (T₀)**
Qué tan dispuesto está SA a aceptar peores soluciones al inicio.
*Alto = más exploración global.*

---
**Cooling rate (α)**
Qué tan rápido "se enfría" SA.
*Cerca de 1.0 = más iteraciones = mejor solución.*

---
**Semilla aleatoria**
Garantiza reproducibilidad.
*Misma semilla = mismo resultado siempre.*
        """)


def _render_presentation_button() -> None:
    """Botón de Modo Presentación (la lógica JS se inyecta desde sections/presentation.py)."""
    st.divider()
    st.button(
        "Modo Presentación",
        use_container_width=True,
        help="Recorre automáticamente las secciones clave (ejecuta la comparación primero).",
        disabled="result_hc" not in st.session_state,
        key="pres_btn",
    )