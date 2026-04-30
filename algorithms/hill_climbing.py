"""
Algoritmo Hill Climbing para problemas de optimización combinatoria.
"""
import time
from typing import Callable, Dict, Any, List

import numpy as np


def hill_climbing(
    initial_solution: List[int],
    cost_fn: Callable[[List[int]], float],
    neighbor_fn: Callable[[List[int], np.random.Generator], List[int]],
    max_iterations: int = 50,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Ejecuta Hill Climbing sobre el problema dado.

    Acepta únicamente movimientos que mejoren la solución actual.
    Se detiene cuando se completan max_iterations iteraciones consecutivas
    sin ninguna mejora (convergencia al óptimo local).

    Parámetros:
        initial_solution: Permutación inicial de nodos.
        cost_fn: Función de costo a minimizar (devuelve float).
        neighbor_fn: Función que genera un vecino dado un estado y un RNG.
        max_iterations: Iteraciones consecutivas sin mejora antes de detenerse.
        seed: Semilla para reproducibilidad del RNG interno.

    Retorna:
        Dict con claves:
            best_solution   — mejor permutación encontrada
            best_value      — costo de esa solución
            iterations      — total de iteraciones ejecutadas
            time_ms         — tiempo total en milisegundos
            history         — lista con el mejor costo en cada iteración
            improvement_pct — porcentaje de mejora respecto a la solución inicial
            converged_at    — iteración donde se encontró la última mejora
    """
    rng = np.random.default_rng(seed)

    current: List[int] = initial_solution.copy()
    current_cost: float = float(cost_fn(current))
    initial_cost: float = current_cost

    best: List[int] = current.copy()
    best_cost: float = current_cost

    history: List[float] = [best_cost]
    no_improve: int = 0
    iteration: int = 0
    last_improve_iter: int = 0

    start = time.perf_counter()

    while no_improve < max_iterations:
        neighbor = neighbor_fn(current, rng)
        neighbor_cost = float(cost_fn(neighbor))

        if neighbor_cost < current_cost:
            current = neighbor
            current_cost = neighbor_cost
            no_improve = 0
            last_improve_iter = iteration
            if current_cost < best_cost:
                best = current.copy()
                best_cost = current_cost
        else:
            no_improve += 1

        history.append(best_cost)
        iteration += 1

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    improvement_pct = (
        (initial_cost - best_cost) / initial_cost * 100.0
        if initial_cost != 0.0
        else 0.0
    )

    return {
        "best_solution": best,
        "best_value": float(best_cost),
        "iterations": int(iteration),
        "time_ms": float(elapsed_ms),
        "history": [float(v) for v in history],
        "improvement_pct": float(improvement_pct),
        "converged_at": int(last_improve_iter),
    }
