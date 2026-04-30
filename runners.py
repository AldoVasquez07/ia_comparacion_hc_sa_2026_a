"""
runners.py
==========
Wrappers cacheados con `st.cache_data` para Hill Climbing y Simulated Annealing.
Aíslan la lógica de instanciación de problemas y permiten que la caché
funcione correctamente cuando los parámetros no cambian.
"""

from typing import Any, Dict

import streamlit as st

from algorithms.hill_climbing import hill_climbing
from algorithms.simulated_annealing import simulated_annealing
from problems.misti_evacuation import problem_instance as misti_instance
from problems.tsp import problem_instance as tsp_instance


def _get_instance(problem_name: str, n: int, seed: int) -> dict:
    """Devuelve la instancia del problema según su nombre."""
    if problem_name == "misti":
        return misti_instance(n, seed)
    return tsp_instance(n, seed)


@st.cache_data(show_spinner=False)
def run_hc(
    problem_name: str,
    n: int,
    seed: int,
    max_iter: int = 50,
) -> Dict[str, Any]:
    """
    Ejecuta Hill Climbing para el problema y parámetros dados.
    El resultado queda cacheado: mismos argumentos → mismo resultado sin recalcular.
    """
    inst = _get_instance(problem_name, n, seed)
    return hill_climbing(
        initial_solution=inst["initial_solution"],
        cost_fn=inst["cost_fn"],
        neighbor_fn=inst["neighbor_fn"],
        max_iterations=max_iter,
        seed=seed,
    )


@st.cache_data(show_spinner=False)
def run_sa(
    problem_name: str,
    n: int,
    seed: int,
    initial_temp: float,
    cooling_rate: float,
    min_temp: float = 0.001,
) -> Dict[str, Any]:
    """
    Ejecuta Simulated Annealing para el problema y parámetros dados.
    El resultado queda cacheado: mismos argumentos → mismo resultado sin recalcular.
    """
    inst = _get_instance(problem_name, n, seed)
    return simulated_annealing(
        initial_solution=inst["initial_solution"],
        cost_fn=inst["cost_fn"],
        neighbor_fn=inst["neighbor_fn"],
        initial_temp=initial_temp,
        cooling_rate=cooling_rate,
        min_temp=min_temp,
        seed=seed,
    )