"""
Problema del Viajero (TSP) con ciudades de coordenadas aleatorias.

Objetivo: encontrar la ruta más corta que visita todas las ciudades
exactamente una vez y regresa al punto de partida.
"""
from typing import Any, Dict, List

import numpy as np


def generate_cities(n: int, seed: int) -> np.ndarray:
    """
    Genera n ciudades con coordenadas aleatorias uniformes en [0, 100].

    Parámetros:
        n: Número de ciudades.
        seed: Semilla para reproducibilidad.

    Retorna:
        Array de forma (n, 2) con coordenadas (x, y) de cada ciudad.
    """
    rng = np.random.default_rng(seed)
    return rng.uniform(0.0, 100.0, size=(n, 2))


def route_distance(solution: List[int], cities: np.ndarray) -> float:
    """
    Calcula la distancia euclidiana total de una ruta circular.

    La ruta visita las ciudades en el orden dado por solution y regresa
    a la ciudad inicial al final.
    """
    total = 0.0
    n = len(solution)
    for i in range(n):
        a = cities[solution[i]]
        b = cities[solution[(i + 1) % n]]
        total += float(np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2))
    return total


def get_initial_solution(n: int, seed: int) -> List[int]:
    """Genera una permutación aleatoria de n ciudades como ruta inicial."""
    rng = np.random.default_rng(seed)
    return list(rng.permutation(n))


def get_neighbor(solution: List[int], rng: np.random.Generator) -> List[int]:
    """
    Genera una ruta vecina intercambiando dos posiciones aleatorias (operador swap).

    Parámetros:
        solution: Ruta actual como permutación de índices de ciudades.
        rng: Generador de números aleatorios de NumPy.

    Retorna:
        Nueva ruta con dos posiciones intercambiadas.
    """
    neighbor = solution.copy()
    i, j = rng.choice(len(solution), size=2, replace=False)
    neighbor[int(i)], neighbor[int(j)] = neighbor[int(j)], neighbor[int(i)]
    return neighbor


def problem_instance(n: int, seed: int) -> Dict[str, Any]:
    """
    Construye la instancia completa del problema TSP con n ciudades.

    Retorna:
        Dict con:
            cities           — array (n, 2) de coordenadas
            initial_solution — ruta inicial aleatoria
            cost_fn          — función de costo lista para usar
            neighbor_fn      — función de vecino lista para usar
            names            — lista de nombres de ciudades
    """
    cities = generate_cities(n, seed)
    initial = get_initial_solution(n, seed)
    return {
        "cities": cities,
        "initial_solution": initial,
        "cost_fn": lambda sol: route_distance(sol, cities),
        "neighbor_fn": get_neighbor,
        "names": [f"Ciudad {i + 1}" for i in range(n)],
    }
