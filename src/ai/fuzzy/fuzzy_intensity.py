"""
fuzzy_intensity.py
------------------
Sistema de inferencia difusa (Mamdani) para determinar
la intensidad de entrenamiento en NeuroFit.

Reimplementación sin skfuzzy — solo numpy.
Lógica idéntica al original: mismas membresías, mismas 10 reglas,
mismo método de defuzzificación (centroide).

Variables de entrada
--------------------
  horas    : horas de entrenamiento por semana  [0 – 20]
  nivel    : "Principiante" | "Intermedio" | "Avanzado"
  animo    : "Desanimado" | "Cansado" | "Normal" | "Bien" | "Excelente"

Variable de salida
------------------
  intensidad : "baja" | "media" | "alta"
"""

import numpy as np


# ---------------------------------------------------------------------------
# Mapeos externos (texto → número)
# ---------------------------------------------------------------------------

NIVEL_MAP = {
    "Principiante": 0.0,
    "Intermedio":   1.0,
    "Avanzado":     2.0,
}

ANIMO_MAP = {
    "Desanimado": 0.0,
    "Cansado":    1.0,
    "Normal":     2.0,
    "Bien":       3.0,
    "Excelente":  4.0,
}


# ---------------------------------------------------------------------------
# Función triangular de membresía
# Incluye correctamente los extremos cuando a==b o b==c
# ---------------------------------------------------------------------------

def _trimf(x: float, abc: list) -> float:
    a, b, c = abc
    if x < a or x > c:
        return 0.0
    if x <= b:
        return 1.0 if b == a else (x - a) / (b - a)
    else:
        return 1.0 if c == b else (c - x) / (c - b)


# ---------------------------------------------------------------------------
# Defuzzificación por centroide
# ---------------------------------------------------------------------------

def _centroid(universe: np.ndarray, aggregated: np.ndarray) -> float:
    den = np.sum(aggregated)
    return float(np.sum(universe * aggregated) / den) if den != 0 else 5.0


# ---------------------------------------------------------------------------
# Función pública
# ---------------------------------------------------------------------------

def determinar_intensidad(animo: str, horas: int, nivel: str) -> str:
    """
    Aplica el sistema difuso Mamdani y devuelve 'baja', 'media' o 'alta'.

    Parámetros
    ----------
    animo  : str — "Desanimado" | "Cansado" | "Normal" | "Bien" | "Excelente"
    horas  : int — horas de entrenamiento por semana (1-20)
    nivel  : str — "Principiante" | "Intermedio" | "Avanzado"
    """

    n = NIVEL_MAP.get(nivel, 1.0)
    a = ANIMO_MAP.get(animo, 2.0)
    h = float(max(0, min(20, horas)))

    # --- Membresías de entrada ---

    h_baja  = _trimf(h, [0,  0,  5])
    h_media = _trimf(h, [3,  7, 12])
    h_alta  = _trimf(h, [9, 20, 20])

    n_prin  = _trimf(n, [0.0, 0.0, 1.0])
    n_inte  = _trimf(n, [0.5, 1.0, 1.5])
    n_avanz = _trimf(n, [1.0, 2.0, 2.0])

    a_bajo  = _trimf(a, [0, 0, 2])
    a_medio = _trimf(a, [1, 2, 3])
    a_alto  = _trimf(a, [2, 4, 4])

    # --- 10 Reglas (Mamdani, AND = min) ---

    r1  = a_bajo                              # R1:  animo bajo  -> baja
    r2  = h_baja                              # R2:  horas bajas -> baja
    r3  = min(n_prin, a_medio)                # R3:  principiante & medio -> baja
    r4  = min(n_prin, a_alto)                 # R4:  principiante & alto  -> media
    r5  = min(n_inte, a_medio)                # R5:  intermedio & medio   -> media
    r6  = min(n_inte, a_alto, h_media)        # R6:  intermedio & alto & horas media -> media
    r7  = min(n_inte, a_alto, h_alta)         # R7:  intermedio & alto & horas alta  -> alta
    r8  = min(n_avanz, a_medio)               # R8:  avanzado & medio     -> media
    r9  = min(n_avanz, a_alto, h_media)       # R9:  avanzado & alto & horas media   -> media
    r10 = min(n_avanz, a_alto, h_alta)        # R10: avanzado & alto & horas alta    -> alta

    # --- Agregacion por consecuente (OR = max) ---

    baja_act  = max(r1, r2, r3)
    media_act = max(r4, r5, r6, r8, r9)
    alta_act  = max(r7, r10)

    # --- Universo de salida y membresias de intensidad ---

    u       = np.arange(0, 10.1, 0.1)
    i_baja  = np.array([_trimf(x, [0,  0,  4]) for x in u])
    i_media = np.array([_trimf(x, [3,  5,  7]) for x in u])
    i_alta  = np.array([_trimf(x, [6, 10, 10]) for x in u])

    # --- Recorte (clipping) y union de las areas ---

    agregado = np.maximum(
        np.minimum(baja_act,  i_baja),
        np.maximum(
            np.minimum(media_act, i_media),
            np.minimum(alta_act,  i_alta),
        )
    )

    # --- Defuzzificacion por centroide ---

    valor = _centroid(u, agregado)

    if valor < 4.0:
        return "baja"
    elif valor > 6.0:
        return "alta"
    else:
        return "media"