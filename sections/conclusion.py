"""
sections/conclusion.py
======================
Renderiza la Sección 6: conclusión automática con métricas clave.
"""

from typing import Any, Dict

import streamlit as st

from config import GRID_COLOR, HC_COLOR, SA_COLOR, WIN_COLOR
from ui.icons import icon as _icon


def render(
    result_hc: Dict[str, Any],
    result_sa: Dict[str, Any],
    sa_is_better: bool,
    diff_pct: float,
    speed_ratio: float,
    prob_display: str,
    n_used: int,
    seed_used: int,
    initial_temp: float,
    cooling_rate: float,
) -> None:
    """
    Muestra la tarjeta de conclusión con el veredicto final del experimento.
    """
    hc_best  = result_hc["best_value"]
    sa_best  = result_sa["best_value"]
    hc_time  = result_hc["time_ms"]
    sa_time  = result_sa["time_ms"]

    # ── Textos dinámicos ──────────────────────────────────────────────────────

    if sa_is_better:
        big_pct   = f"+{diff_pct:.1f}%"
        big_color = WIN_COLOR
        big_label = "MEJOR  (SA vs HC)"
        b1_text = f"SA encontró una solución <b>{diff_pct:.1f}% mejor</b> que Hill Climbing en {prob_display}"
    else:
        big_pct   = f"+{diff_pct:.1f}%"
        big_color = HC_COLOR
        big_label = "MEJOR  (HC vs SA)"
        b1_text = (
            f"HC encontró una solución <b>{diff_pct:.1f}% mejor</b> que Simulated Annealing en {prob_display}"
            if diff_pct >= 0.01
            else f"HC y SA encontraron la <b>misma calidad</b> de solución en {prob_display}"
        )

    if speed_ratio > 1.1:
        b2_text = f"HC fue <b>{speed_ratio:.1f}x más rápido</b> ({hc_time:.0f} ms vs {sa_time:.0f} ms)"
    elif speed_ratio < 0.9:
        b2_text = f"SA fue <b>{1/speed_ratio:.1f}x más rápido</b> ({sa_time:.0f} ms vs {hc_time:.0f} ms)"
    else:
        b2_text = f"Ambos algoritmos tuvieron tiempos <b>similares</b> ({hc_time:.0f} ms vs {sa_time:.0f} ms)"

    if sa_is_better and n_used >= 10:
        b3_text = (
            f"Para N={n_used}, <b>SA es claramente superior</b> — "
            "la diferencia de calidad justifica el tiempo extra"
        )
    elif sa_is_better:
        b3_text = f"Incluso con N={n_used}, SA supera a HC gracias a su exploración probabilística"
    else:
        b3_text = f"Para N={n_used}, <b>HC es suficiente</b> — SA no añade ventaja cuando el espacio es pequeño"

    para_llevar = (
        "SA sacrifica velocidad para escapar trampas locales — vale la pena cuando N es grande."
        if sa_is_better else
        "HC converge rápido y bien cuando el espacio de búsqueda es pequeño — úsalo primero."
    )
    para_color = WIN_COLOR if sa_is_better else HC_COLOR

    ico_check = _icon("check-circle", size=15, color=WIN_COLOR,  style="margin-right:6px;flex-shrink:0;")
    ico_zap   = _icon("zap",          size=15, color="#CBD5E0",  style="margin-right:6px;flex-shrink:0;")
    ico_target = _icon("target",      size=15, color="#CBD5E0",  style="margin-right:6px;flex-shrink:0;")
    ico_bulb  = _icon("lightbulb",    size=16, color=para_color, style="margin-right:8px;flex-shrink:0;")
    ico_cpu   = _icon("cpu",          size=12, color="#8892A4",  style="margin-right:4px;vertical-align:-1px;")

    b1 = f'<span style="display:flex;align-items:center;">{ico_check}{b1_text}</span>'
    b2 = f'<span style="display:flex;align-items:center;">{ico_zap}{b2_text}</span>'
    b3 = f'<span style="display:flex;align-items:center;">{ico_target}{b3_text}</span>'

    st.subheader("Conclusión Automática")
    st.markdown(
        f"""
<div class="conclusion-card">
  <div style="display:flex; align-items:center; gap:2rem; margin-bottom:20px; flex-wrap:wrap;">
    <div style="text-align:center; min-width:110px;">
      <div style="font-size:52px; font-weight:900; color:{big_color}; line-height:1.1;">{big_pct}</div>
      <div style="color:{big_color}; font-size:11px; font-weight:700; letter-spacing:0.06em; margin-top:4px;">{big_label}</div>
    </div>
    <div style="flex:1; min-width:220px; display:flex; flex-direction:column; gap:6px;">
      <p style="color:#CBD5E0; font-size:14px; line-height:1.9; margin:0;">{b1}</p>
      <p style="color:#CBD5E0; font-size:14px; line-height:1.9; margin:0;">{b2}</p>
      <p style="color:#CBD5E0; font-size:14px; line-height:1.9; margin:0;">{b3}</p>
    </div>
  </div>
  <hr style="border-color:{GRID_COLOR}; margin:16px 0 14px 0;">
  <p style="font-size:17px; font-weight:800; color:{para_color}; margin:0 0 12px 0;
            letter-spacing:-0.01em; display:flex; align-items:center;">
    {ico_bulb}{para_llevar}
  </p>
  <p style="color:#8892A4; font-size:11px; margin:0; display:flex; align-items:center; gap:4px;">
    {ico_cpu}
    HC={hc_best:.5f} &nbsp;|&nbsp; SA={sa_best:.5f} &nbsp;|&nbsp;
    N={n_used} &nbsp;|&nbsp; seed={seed_used} &nbsp;|&nbsp;
    T₀={initial_temp:.0f} &nbsp;|&nbsp; α={cooling_rate:.3f}
  </p>
</div>
""",
        unsafe_allow_html=True,
    )