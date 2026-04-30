"""
app.py
======
Punto de entrada de la aplicación. Su único trabajo es:
  1. Configurar la página.
  2. Inyectar estilos.
  3. Renderizar el sidebar y obtener parámetros.
  4. Ejecutar los algoritmos si el usuario lo solicita.
  5. Llamar a cada sección en orden.

No contiene lógica de negocio, HTML ni figuras Plotly.
"""

import streamlit as st

# ── Configuración de página (debe ir antes de cualquier otro st.*) ────────────

st.set_page_config(
    page_title="Optimización: HC vs SA | Arequipa 2026",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Módulos propios ───────────────────────────────────────────────────────────

import ui.styles as styles
import sections.sidebar      as sidebar
import sections.hero         as hero
import sections.guide        as guide
import sections.metrics      as metrics
import sections.convergence  as convergence
import sections.comparison   as comparison
import sections.map     as map_view
import sections.sensitivity  as sensitivity
import sections.conclusion   as conclusion
import sections.scale        as scale
import sections.presentation as presentation

from runners import run_hc, run_sa

# ── Estilos globales ──────────────────────────────────────────────────────────

styles.inject()

# ── Cabecera ──────────────────────────────────────────────────────────────────

from ui.icons import icon as _icon

_ico_brain = _icon("cpu", size=28, color="#E2E8F0", style="margin-right:10px;vertical-align:-5px;")
st.markdown(
    f'<h1 style="display:flex;align-items:center;">{_ico_brain}Optimización Metaheurística</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "**Hill Climbing vs Simulated Annealing** — Comparativa en tiempo real"
    " &nbsp;|&nbsp; Arequipa 2026"
)
st.divider()

# ── Sidebar → parámetros ──────────────────────────────────────────────────────

problem_name, problem_label, n, seed, initial_temp, cooling_rate, run_clicked = sidebar.render()

# ── Secciones estáticas (visibles siempre) ────────────────────────────────────

hero.render(problem_name, n)
guide.render()

# ── Ejecutar algoritmos ───────────────────────────────────────────────────────

MIN_TEMP = 0.001

if run_clicked:
    with st.spinner("Ejecutando Hill Climbing..."):
        result_hc = run_hc(problem_name, n, seed)

    prog = st.progress(0, text="Ejecutando Simulated Annealing...")
    with st.spinner(""):
        result_sa = run_sa(problem_name, n, seed, initial_temp, cooling_rate, MIN_TEMP)
    prog.progress(1.0, text="¡Completado!")

    st.session_state.update({
        "result_hc":    result_hc,
        "result_sa":    result_sa,
        "problem_name": problem_name,
        "n_used":       n,
        "seed_used":    seed,
        "initial_temp": initial_temp,
        "cooling_rate": cooling_rate,
    })
    st.balloons()

# ── Sin resultados todavía ────────────────────────────────────────────────────

if "result_hc" not in st.session_state:
    st.info(
        "Configura los parámetros en el panel lateral y pulsa "
        "**▶ Ejecutar Comparación** para comenzar."
    )
    st.stop()

# ── Recuperar estado ──────────────────────────────────────────────────────────

result_hc    = st.session_state["result_hc"]
result_sa    = st.session_state["result_sa"]
prob_name    = st.session_state["problem_name"]
n_used       = st.session_state["n_used"]
seed_used    = st.session_state["seed_used"]
initial_temp = st.session_state["initial_temp"]
cooling_rate = st.session_state["cooling_rate"]

hc_best  = result_hc["best_value"]
sa_best  = result_sa["best_value"]
hc_time  = result_hc["time_ms"]
sa_time  = result_sa["time_ms"]
hc_iters = result_hc["iterations"]
sa_iters = result_sa["iterations"]
hc_improv = result_hc["improvement_pct"]
sa_improv = result_sa["improvement_pct"]

# Ganadores por métrica
winner_val   = "hc" if hc_best  < sa_best  else ("sa" if sa_best  < hc_best  else "tie")
winner_time  = "hc" if hc_time  < sa_time  else "sa"
winner_iters = "hc" if hc_iters < sa_iters else "sa"
winner_improv = "hc" if hc_improv > sa_improv else "sa"

sa_is_better = sa_best < hc_best
diff_pct     = abs(hc_best - sa_best) / max(abs(hc_best), 1e-9) * 100.0
speed_ratio  = sa_time / hc_time if hc_time > 0.0 else 1.0
prob_display = "Evacuación del Misti" if prob_name == "misti" else "TSP"

# ── Secciones con resultados ──────────────────────────────────────────────────

metrics.render(
    result_hc, result_sa,
    winner_val, winner_time, winner_iters, winner_improv,
    sa_is_better, diff_pct, speed_ratio, prob_display, n_used,
)

convergence.render(result_hc, result_sa, winner_val)

comparison.render(
    result_hc, result_sa,
    winner_val, winner_time,
    sa_is_better, diff_pct, speed_ratio,
)

map_view.render(
    prob_name, result_hc, result_sa,
    n_used, seed_used, sa_is_better, diff_pct,
)

sensitivity.render(prob_name, n_used, seed_used)

conclusion.render(
    result_hc, result_sa,
    sa_is_better, diff_pct, speed_ratio,
    prob_display, n_used, seed_used, initial_temp, cooling_rate,
)

scale.render(seed_used, initial_temp, cooling_rate)

presentation.render()