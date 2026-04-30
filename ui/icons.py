"""
ui/icons.py
===========
Íconos Lucide como SVG inline.
Uso:  from ui.icons import icon
      icon("target")          → SVG 16×16 con color heredado
      icon("target", size=20) → SVG 20×20
      icon("target", color="#F4A261") → color explícito
"""

from typing import Optional

# ── Paths de cada ícono (stroke, no fill) ────────────────────────────────────
# Cada valor es el contenido interno del <svg> (solo los <path>/<circle>/<line>…)

_PATHS: dict[str, str] = {
    # Métricas
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polyline points="12 6 12 12 16 14"/>'
    ),
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "trending-up": (
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
        '<polyline points="17 6 23 6 23 12"/>'
    ),

    # Algoritmos
    "mountain": (
        '<path d="M8 3L1 21h22L15 3z"/>'
        '<path d="M12 8l4 8H8l4-8z" fill="currentColor" stroke="none" opacity="0.3"/>'
    ),
    "thermometer": (
        '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>'
    ),

    # Navegación / acciones
    "play": '<polygon points="5 3 19 12 5 21 5 3"/>',
    "refresh-cw": (
        '<polyline points="23 4 23 10 17 10"/>'
        '<polyline points="1 20 1 14 7 14"/>'
        '<path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>'
    ),
    "settings": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06'
        'a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09'
        'A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83'
        'l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09'
        'A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83'
        'l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09'
        'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83'
        'l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09'
        'a1.65 1.65 0 0 0-1.51 1z"/>'
    ),
    "sliders": (
        '<line x1="4" y1="21" x2="4" y2="14"/>'
        '<line x1="4" y1="10" x2="4" y2="3"/>'
        '<line x1="12" y1="21" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12" y2="3"/>'
        '<line x1="20" y1="21" x2="20" y2="16"/>'
        '<line x1="20" y1="12" x2="20" y2="3"/>'
        '<line x1="1" y1="14" x2="7" y2="14"/>'
        '<line x1="9" y1="8" x2="15" y2="8"/>'
        '<line x1="17" y1="16" x2="23" y2="16"/>'
    ),
    "presentation": (
        '<path d="M2 3h20"/>'
        '<path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/>'
        '<path d="M7 21l5-5 5 5"/>'
    ),

    # Análisis
    "bar-chart-2": (
        '<line x1="18" y1="20" x2="18" y2="10"/>'
        '<line x1="12" y1="20" x2="12" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="14"/>'
    ),
    "line-chart": (
        '<line x1="0" y1="0" x2="0" y2="24" stroke="none"/>'  # placeholder
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
    ),
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "map": (
        '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>'
        '<line x1="8" y1="2" x2="8" y2="18"/>'
        '<line x1="16" y1="6" x2="16" y2="22"/>'
    ),
    "flag": (
        '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>'
        '<line x1="4" y1="22" x2="4" y2="15"/>'
    ),

    # Info / estado
    "info": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="8" x2="12" y2="12"/>'
        '<line x1="12" y1="16" x2="12.01" y2="16"/>'
    ),
    "award": (
        '<circle cx="12" cy="8" r="6"/>'
        '<path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/>'
    ),
    "check-circle": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
        '<polyline points="22 4 12 14.01 9 11.01"/>'
    ),
    "alert-triangle": (
        '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3'
        'L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
        '<line x1="12" y1="9" x2="12" y2="13"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>'
    ),
    "lightbulb": (
        '<path d="M9 18h6"/>'
        '<path d="M10 22h4"/>'
        '<path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>'
    ),
    "cpu": (
        '<rect x="4" y="4" width="16" height="16" rx="2"/>'
        '<rect x="9" y="9" width="6" height="6"/>'
        '<line x1="9" y1="1" x2="9" y2="4"/>'
        '<line x1="15" y1="1" x2="15" y2="4"/>'
        '<line x1="9" y1="20" x2="9" y2="23"/>'
        '<line x1="15" y1="20" x2="15" y2="23"/>'
        '<line x1="20" y1="9" x2="23" y2="9"/>'
        '<line x1="20" y1="14" x2="23" y2="14"/>'
        '<line x1="1" y1="9" x2="4" y2="9"/>'
        '<line x1="1" y1="14" x2="4" y2="14"/>'
    ),
    "microscope": (
        '<path d="M6 18h8"/>'
        '<path d="M3 22h18"/>'
        '<path d="M14 22a7 7 0 1 0 0-14h-1"/>'
        '<path d="M9 14l-1-7"/>'
        '<path d="M11.7 7H9.6a.5.5 0 0 1-.46-.69L10 4h4l1 2.31a.5.5 0 0 1-.46.69h-2.84z"/>'
    ),
    "book-open": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "volcano": (   # Lucide no tiene volcano — usamos "flame" como sustituto
        '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 '
        '.5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'
    ),
    "route": (
        '<circle cx="6" cy="19" r="3"/>'
        '<path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/>'
        '<circle cx="18" cy="5" r="3"/>'
    ),
    "compass": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/>'
        '<polyline points="2 12 12 17 22 12"/>'
    ),
}


# ── Función pública ───────────────────────────────────────────────────────────

def icon(
    name: str,
    size: int = 16,
    color: Optional[str] = None,
    style: str = "",
    cls: str = "",
) -> str:
    """
    Devuelve el SVG inline de un ícono Lucide.

    Args:
        name:   Clave del ícono (ver _PATHS).
        size:   Ancho y alto en px (default 16).
        color:  Color del trazo. Si es None, hereda `currentColor`.
        style:  Estilos CSS adicionales para el <svg>.
        cls:    Clases CSS adicionales para el <svg>.

    Returns:
        String HTML con el <svg> listo para insertar en markdown unsafe.
    """
    paths = _PATHS.get(name, _PATHS["info"])
    stroke = color if color else "currentColor"
    base_style = f"display:inline-block;vertical-align:middle;flex-shrink:0;{style}"
    class_attr = f' class="{cls}"' if cls else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'style="{base_style}"{class_attr}>'
        f'{paths}'
        f'</svg>'
    )