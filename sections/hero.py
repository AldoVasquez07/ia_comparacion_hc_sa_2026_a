"""
sections/hero.py
================
Renderiza el bloque "hero" que describe el problema actual.
"""

import streamlit as st
from config import HC_COLOR, SA_COLOR
from ui.icons import icon as _icon


def render(problem_name: str, n: int) -> None:
    if problem_name == "misti":
        desc = (
            f"El volcán Misti amenaza Arequipa. Hay <b>{n} distritos</b> en peligro. "
            "¿En qué <b>ORDEN</b> evacuamos para minimizar el riesgo total acumulado?"
        )
    else:
        desc = (
            f"Hay <b>{n} ciudades</b> que visitar exactamente una vez. "
            "¿Cuál es la <b>RUTA MÁS CORTA</b> que pasa por todas y regresa al origen?"
        )

    ico_title  = _icon("layers",      size=20, color=SA_COLOR, style="margin-right:10px;")
    ico_hc     = _icon("mountain",    size=36, color=HC_COLOR)
    ico_sa     = _icon("thermometer", size=36, color=SA_COLOR)

    st.markdown(
        f"""
<div style="background: linear-gradient(135deg, #1a1d2e, #2d1b3d);
     border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem;
     border-left: 4px solid {SA_COLOR};">
  <h2 style="color: {SA_COLOR}; margin: 0 0 0.5rem; font-size: 1.3rem;
             display:flex; align-items:center;">
    {ico_title}¿Qué estamos resolviendo?
  </h2>
  <p style="color: #ccc; font-size: 1.05rem; margin: 0 0 1.5rem;">{desc}</p>
  <div style="display: flex; gap: 2.5rem; flex-wrap: wrap;">
    <div style="text-align: center; min-width: 140px;">
      {ico_hc}
      <br>
      <b style="color: {HC_COLOR}; font-size: 1rem;">Hill Climbing</b>
      <p style="color: #aaa; font-size: 0.85rem; margin: 0.4rem 0 0; line-height: 1.5;">
        Acepta solo mejoras.<br>Rápido, pero queda<br>
        <b style="color:{HC_COLOR}">atrapado en óptimos locales.</b>
      </p>
    </div>
    <div style="font-size: 2rem; align-self: center; color: #555; font-weight: 900;">VS</div>
    <div style="text-align: center; min-width: 140px;">
      {ico_sa}
      <br>
      <b style="color: {SA_COLOR}; font-size: 1rem;">Simulated Annealing</b>
      <p style="color: #aaa; font-size: 0.85rem; margin: 0.4rem 0 0; line-height: 1.5;">
        A veces acepta empeorar<br>para escapar trampas.<br>
        <b style="color:{SA_COLOR}">Encuentra mejores soluciones.</b>
      </p>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )