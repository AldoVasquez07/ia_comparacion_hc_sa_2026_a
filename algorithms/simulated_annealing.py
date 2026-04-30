"""
Algoritmo Simulated Annealing para problemas de optimización combinatoria.
"""
import math
import time
from typing import Callable, Dict, Any, List

import numpy as np


def simulated_annealing(
    initial_solution: List[int],
    cost_fn: Callable[[List[int]], float],
    neighbor_fn: Callable[[List[int], np.random.Generator], List[int]],
    initial_temp: float = 500.0,
    cooling_rate: float = 0.995,
    min_temp: float = 0.001,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Ejecuta Simulated Annealing sobre el problema dado.

    Acepta mejoras siempre. Acepta soluciones peores con probabilidad
    P = e^(-Δ/T), donde Δ es el incremento de costo y T la temperatura actual.
    La temperatura decrece cada iteración: T ← T × cooling_rate.
    El algoritmo se detiene cuando T < min_temp.

    Parámetros:
        initial_solution: Permutación inicial de nodos (misma que HC).
        cost_fn: Función de costo a minimizar (devuelve float).
        neighbor_fn: Función que genera un vecino dado un estado y un RNG.
        initial_temp: Temperatura inicial T₀.
        cooling_rate: Factor de enfriamiento por iteración (0 < α < 1).
        min_temp: Temperatura mínima para detener el algoritmo.
        seed: Semilla para reproducibilidad del RNG interno.

    Retorna:
        Dict con claves:
            best_solution       — mejor permutación encontrada
            best_value          — costo de esa solución
            iterations          — total de iteraciones ejecutadas
            time_ms             — tiempo total en milisegundos
            history             — mejor costo en cada iteración
            improvement_pct     — porcentaje de mejora respecto a la solución inicial
            temperature_history — temperatura en cada iteración
    """
    rng = np.random.default_rng(seed)

    current: List[int] = initial_solution.copy()
    current_cost: float = float(cost_fn(current))
    initial_cost: float = current_cost

    best: List[int] = current.copy()
    best_cost: float = current_cost

    T: float = initial_temp
    history: List[float] = [best_cost]
    temp_history: List[float] = [T]
    iteration: int = 0

    start = time.perf_counter()

    while T > min_temp:
        neighbor = neighbor_fn(current, rng)
        neighbor_cost = float(cost_fn(neighbor))
        delta = neighbor_cost - current_cost

        if delta < 0.0 or rng.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = current.copy()
                best_cost = current_cost

        T *= cooling_rate
        iteration += 1
        history.append(best_cost)
        temp_history.append(T)

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
        "temperature_history": [float(t) for t in temp_history],
    }
