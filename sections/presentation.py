"""
sections/presentation.py
========================
Inyecta el JavaScript del Modo Presentación cuando el botón está activo.
"""

import streamlit as st
import streamlit.components.v1 as components

from config import SA_COLOR


_STEPS = [
    "¿Qué estamos resolviendo?",
    "Resultados de la Comparación",
    "Convergencia de la Solución",
    "SA vs HC a escala",
    "Conclusión Automática",
]


def render() -> None:
    """Inyecta el JS de presentación si el botón fue pulsado en este ciclo."""
    if not st.session_state.get("pres_btn"):
        return

    steps_js = str(_STEPS).replace("'", '"')

    components.html(
        f"""
        <script>
        (function () {{
            var pd = window.parent.document;

            if (!pd.getElementById('pres-style')) {{
                var s = pd.createElement('style');
                s.id = 'pres-style';
                s.textContent = [
                    '@keyframes glow-pulse {{',
                    '  0%   {{ box-shadow: 0 0 8px rgba(244,162,97,0.4); }}',
                    '  50%  {{ box-shadow: 0 0 40px rgba(244,162,97,0.85), 0 0 70px rgba(244,162,97,0.35); }}',
                    '  100% {{ box-shadow: 0 0 8px rgba(244,162,97,0.4); }}',
                    '}}',
                    '.pres-highlight {{',
                    '  animation: glow-pulse 1.4s ease-in-out infinite !important;',
                    '  outline: 2px solid {SA_COLOR} !important;',
                    '  outline-offset: 6px !important;',
                    '  border-radius: 10px !important;',
                    '}}'
                ].join('');
                pd.head.appendChild(s);
            }}

            function clearGlow() {{
                pd.querySelectorAll('.pres-highlight').forEach(function(el) {{
                    el.classList.remove('pres-highlight');
                }});
            }}

            function findHeader(text) {{
                var els = Array.from(pd.querySelectorAll('h1,h2,h3,p'));
                return els.find(function(h) {{ return h.textContent.includes(text); }});
            }}

            function highlightAndScroll(text) {{
                clearGlow();
                var h = findHeader(text);
                if (!h) return;
                var el = h;
                for (var i = 0; i < 6; i++) {{
                    if (el.parentElement) el = el.parentElement;
                    else break;
                }}
                el.classList.add('pres-highlight');
                h.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}

            var steps = {steps_js};
            var i = 0;
            function next() {{
                if (i >= steps.length) {{ clearGlow(); return; }}
                highlightAndScroll(steps[i]);
                i++;
                setTimeout(next, 3000);
            }}
            setTimeout(next, 400);
        }})();
        </script>
        """,
        height=0,
    )