"""
sections/map_view.py
====================
Renderiza la Sección 4: visualización de rutas sobre el mapa.
Maneja tanto el problema TSP como el de Evacuación del Misti.
"""

from typing import Any, Dict

import streamlit as st

from charts import build_misti_figure, build_tsp_figure
from config import HC_COLOR, SA_COLOR
from problems.misti_evacuation import compute_danger, get_districts
from problems.tsp import generate_cities


def render(
    prob_name: str,
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    n_used: int,
    seed_used: int,
    sa_is_better: bool,
    diff_pct: float,
) -> None:
    """
    Muestra las rutas de HC y SA en pestañas separadas.

    Args:
        prob_name:    "misti" o "tsp".
        result_hc/sa: Resultados de los algoritmos.
        n_used:       N del experimento.
        seed_used:    Semilla usada.
        sa_is_better: True si SA encontró mejor valor.
        diff_pct:     Diferencia porcentual.
    """
    st.subheader("🗺️ Visualización de Rutas")

    if prob_name == "tsp":
        _render_tsp(result_hc, result_sa, n_used, seed_used, sa_is_better, diff_pct)
    else:
        _render_misti(result_hc, result_sa, n_used, sa_is_better, diff_pct)


# ── Helpers internos ──────────────────────────────────────────────────────────

def _render_tsp(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    n_used: int,
    seed_used: int,
    sa_is_better: bool,
    diff_pct: float,
) -> None:
    st.markdown(
        "**¿Cómo recorren las ciudades los algoritmos?**  \n"
        "Los números indican el **orden de visita**. "
        "El gradiente de color va del inicio (claro) al final (oscuro) de la ruta."
    )

    cities = generate_cities(n_used, seed_used)

    tab_hc, tab_sa = st.tabs(["🔵 Hill Climbing", "🟠 Simulated Annealing"])

    with tab_hc:
        fig = build_tsp_figure(
            result_hc["best_solution"], cities,
            "Ruta Hill Climbing", HC_COLOR, "Blues_r",
        )
        st.plotly_chart(fig, use_container_width=True)
        route_names = [f"C{i+1}" for i in result_hc["best_solution"]]
        st.markdown(
            f"**HC recorre:** {' → '.join(route_names)} → {route_names[0]}  \n"
            f"**Distancia total:** `{result_hc['best_value']:.2f}` unidades"
        )

    with tab_sa:
        fig = build_tsp_figure(
            result_sa["best_solution"], cities,
            "Ruta Simulated Annealing", SA_COLOR, "Oranges_r",
        )
        st.plotly_chart(fig, use_container_width=True)
        route_names = [f"C{i+1}" for i in result_sa["best_solution"]]
        st.markdown(
            f"**SA recorre:** {' → '.join(route_names)} → {route_names[0]}  \n"
            f"**Distancia total:** `{result_sa['best_value']:.2f}` unidades"
        )

    if result_hc["best_solution"] == result_sa["best_solution"]:
        st.success("HC y SA encontraron exactamente la misma ruta.")
    else:
        better = "SA" if sa_is_better else "HC"
        st.info(
            f"HC y SA encontraron rutas **diferentes**. "
            f"**{better}** logró la ruta más corta ({diff_pct:.1f}% mejor)."
        )


def _render_misti(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    n_used: int,
    sa_is_better: bool,
    diff_pct: float,
) -> None:
    st.markdown(
        "**¿Cómo evacuan los algoritmos? — Orden real en el mapa de Arequipa**  \n"
        "El número dentro de cada punto indica el **orden de evacuación**. "
        "Los colores muestran el **nivel de peligro** "
        "(🔴 rojo = más cerca al Misti = más urgente evacuar primero)."
    )

    districts = get_districts(n_used)
    dangers   = compute_danger(districts)

    tab_hc, tab_sa = st.tabs(["🔵 Hill Climbing", "🟠 Simulated Annealing"])

    with tab_hc:
        fig = build_misti_figure(
            result_hc["best_solution"], districts, dangers,
            "Orden de Evacuación — Hill Climbing", HC_COLOR,
        )
        st.plotly_chart(fig, use_container_width=True)
        evac = [districts[i]["name"] for i in result_hc["best_solution"]]
        st.markdown(
            f"**HC evacúa en este orden:** {' → '.join(evac)}  \n"
            f"**Costo total acumulado:** `{result_hc['best_value']:.4f}`"
        )

    with tab_sa:
        fig = build_misti_figure(
            result_sa["best_solution"], districts, dangers,
            "Orden de Evacuación — Simulated Annealing", SA_COLOR,
        )
        st.plotly_chart(fig, use_container_width=True)
        evac = [districts[i]["name"] for i in result_sa["best_solution"]]
        st.markdown(
            f"**SA evacúa en este orden:** {' → '.join(evac)}  \n"
            f"**Costo total acumulado:** `{result_sa['best_value']:.4f}`"
        )

    if result_hc["best_solution"] == result_sa["best_solution"]:
        st.success("HC y SA encontraron el **mismo orden** de evacuación.")
    else:
        better = "SA" if sa_is_better else "HC"
        st.info(
            f"HC y SA encontraron **órdenes distintos**. "
            f"**{better}** encontró el orden con menor peligro acumulado "
            f"({diff_pct:.1f}% mejor)."
        )