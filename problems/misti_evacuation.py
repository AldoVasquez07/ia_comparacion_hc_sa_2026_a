"""
Problema de Evacuación del Volcán Misti — Arequipa, Perú.

Objetivo: encontrar el orden óptimo para evacuar distritos de Arequipa
minimizando el peligro acumulado total. Los distritos más cercanos al Misti
son más peligrosos y deben evacuarse primero.
"""
from typing import Any, Callable, Dict, List

import numpy as np

# Coordenadas del volcán Misti
MISTI_LAT: float = -16.294
MISTI_LON: float = -71.409

# Distritos de Arequipa con coordenadas reales
DISTRICTS: List[Dict[str, Any]] = [
    {"name": "Cercado",        "lat": -16.398, "lon": -71.537},
    {"name": "Miraflores",     "lat": -16.379, "lon": -71.514},
    {"name": "Cayma",          "lat": -16.365, "lon": -71.561},
    {"name": "Yanahuara",      "lat": -16.383, "lon": -71.551},
    {"name": "Cerro Colorado", "lat": -16.333, "lon": -71.570},
    {"name": "Sachaca",        "lat": -16.420, "lon": -71.570},
    {"name": "Tiabaya",        "lat": -16.440, "lon": -71.571},
    {"name": "Uchumayo",       "lat": -16.449, "lon": -71.606},
    {"name": "Mariano Melgar", "lat": -16.388, "lon": -71.509},
    {"name": "Paucarpata",     "lat": -16.420, "lon": -71.509},
]


def get_districts(n: int) -> List[Dict[str, Any]]:
    """Retorna los primeros n distritos de la lista maestra."""
    return DISTRICTS[:n]


def compute_danger(districts: List[Dict[str, Any]]) -> np.ndarray:
    """
    Calcula el nivel de peligro de cada distrito.

    Peligro = 1 / distancia_euclidiana_al_Misti.
    Distritos más cercanos al Misti reciben un valor de peligro mayor.
    """
    dangers = []
    for d in districts:
        dist = np.sqrt(
            (d["lat"] - MISTI_LAT) ** 2 + (d["lon"] - MISTI_LON) ** 2
        )
        dangers.append(1.0 / dist)
    return np.array(dangers)


def evacuation_cost(solution: List[int], dangers: np.ndarray) -> float:
    """
    Costo total de una orden de evacuación.

    Fórmula: Σ danger[solution[i]] × (i + 1)

    Evacuar primero los distritos más peligrosos (danger alto)
    asigna un multiplicador de posición bajo, reduciendo el costo total.
    El óptimo teórico es ordenar de mayor a menor peligro.
    """
    total = 0.0
    for i, idx in enumerate(solution):
        total += dangers[idx] * (i + 1)
    return total


def get_initial_solution(n: int, seed: int) -> List[int]:
    """Genera una permutación aleatoria de n distritos como solución inicial."""
    rng = np.random.default_rng(seed)
    return list(rng.permutation(n))


def get_neighbor(solution: List[int], rng: np.random.Generator) -> List[int]:
    """
    Genera un vecino intercambiando dos posiciones aleatorias (operador swap).

    Parámetros:
        solution: Permutación actual.
        rng: Generador de números aleatorios de NumPy.

    Retorna:
        Nueva permutación con dos posiciones intercambiadas.
    """
    neighbor = solution.copy()
    i, j = rng.choice(len(solution), size=2, replace=False)
    neighbor[int(i)], neighbor[int(j)] = neighbor[int(j)], neighbor[int(i)]
    return neighbor


def problem_instance(n: int, seed: int) -> Dict[str, Any]:
    """
    Construye la instancia completa del problema Misti con n distritos.

    Retorna:
        Dict con:
            districts        — lista de distritos con nombre y coordenadas
            dangers          — array de niveles de peligro (1/dist_al_Misti)
            initial_solution — permutación aleatoria inicial
            cost_fn          — función de costo lista para usar
            neighbor_fn      — función de vecino lista para usar
            names            — lista de nombres de distritos
    """
    districts = get_districts(n)
    dangers = compute_danger(districts)
    initial = get_initial_solution(n, seed)
    return {
        "districts": districts,
        "dangers": dangers,
        "initial_solution": initial,
        "cost_fn": lambda sol: evacuation_cost(sol, dangers),
        "neighbor_fn": get_neighbor,
        "names": [d["name"] for d in districts],
    }
