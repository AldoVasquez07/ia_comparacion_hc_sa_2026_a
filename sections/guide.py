"""
sections/guide.py
=================
Expander con la guía didáctica HC vs SA para la presentación.
"""

import pandas as pd
import streamlit as st


def render() -> None:
    """Muestra el expander 'Guía para la Presentación'."""
    with st.expander("Guía para la Presentación", expanded=False):
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
### ¿Por qué comparar HC vs SA?

Imagina un **montañista** en un paisaje invertido: buscamos el *valle más profundo*
(costo mínimo), no la cima.

- **Hill Climbing** camina siempre cuesta abajo. Si llega a un hoyo local,
  se queda atrapado para siempre. Es rápido, pero miope.
- **Simulated Annealing** a veces *sube una colina* para escapar de hoyos locales
  y encontrar valles más profundos. Inspirado en el enfriamiento lento del metal.

#### Fórmula de aceptación SA
""")
            st.latex(r"P(\text{aceptar solución peor}) = e^{-\Delta / T}")
            st.markdown("""
| Variable | Significado |
|----------|-------------|
| Δ | Incremento de costo (empeoramiento) |
| T | Temperatura actual |

Con **T alto** → probabilidad alta de aceptar peores → exploración global.
Con **T bajo** → probabilidad baja → explotación local (como HC).
""")

        with col2:
            st.markdown("### Tabla comparativa HC vs SA")
            df = pd.DataFrame({
                "Aspecto": [
                    "Acepta soluciones peores",
                    "Riesgo de óptimo local",
                    "Velocidad de ejecución",
                    "Parámetros requeridos",
                    "Calidad de solución final",
                    "Determinismo",
                ],
                "Hill Climbing": [
                    "Nunca", "Alto", "Muy rápido",
                    "Ninguno", "Buena (local)", "Sí (dado seed)",
                ],
                "Simulated Annealing": [
                    "Sí (con probabilidad)", "Bajo", "Moderado",
                    "T₀, α, T_min", "Excelente (global)", "Sí (dado seed)",
                ],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.info(
                "**En el Misti:** HC se queda atrapado en el primer orden "
                "'suficientemente bueno'. SA explora más el espacio y encuentra "
                "el orden óptimo real de evacuación."
            )
            st.warning(
                "**Tip de presentación:** varía el cooling rate de 0.90 a 0.999 "
                "y observa cómo cambia tanto la calidad de la solución como el "
                "número de iteraciones necesarias."
            )