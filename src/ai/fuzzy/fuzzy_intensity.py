"""
fuzzy_intensity.py
------------------
Sistema de inferencia difusa (Mamdani) para determinar
la intensidad de entrenamiento en NeuroFit.

Variables de entrada
--------------------
  horas    : horas de entrenamiento por semana  [0 – 20]
  nivel_n  : nivel físico codificado            [0=Principiante, 1=Intermedio, 2=Avanzado]
  animo_n  : estado de ánimo codificado         [0=Desanimado, 1=Cansado, 2=Normal, 3=Bien, 4=Excelente]

Variable de salida
------------------
  intensidad : valor numérico [0 – 10]
               < 4  → "baja"
               4–6  → "media"
               > 6  → "alta"

Reglas (10 en total)
--------------------
  R1 : SI ánimo ES bajo             → intensidad ES baja
  R2 : SI horas ES baja             → intensidad ES baja
  R3 : SI nivel ES principiante Y ánimo ES medio  → intensidad ES baja
  R4 : SI nivel ES principiante Y ánimo ES alto   → intensidad ES media
  R5 : SI nivel ES intermedio Y ánimo ES medio    → intensidad ES media
  R6 : SI nivel ES intermedio Y ánimo ES alto Y horas ES media → intensidad ES media
  R7 : SI nivel ES intermedio Y ánimo ES alto Y horas ES alta  → intensidad ES alta
  R8 : SI nivel ES avanzado Y ánimo ES medio      → intensidad ES media
  R9 : SI nivel ES avanzado Y ánimo ES alto Y horas ES media   → intensidad ES media
  R10: SI nivel ES avanzado Y ánimo ES alto Y horas ES alta    → intensidad ES alta
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ---------------------------------------------------------------------------
# Mapeos externos  (texto → número)
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
# Construcción del sistema difuso (se hace una sola vez al importar)
# ---------------------------------------------------------------------------

def _construir_sistema():
    # --- Antecedentes ---
    h = ctrl.Antecedent(np.arange(0, 21, 1),     'horas')
    n = ctrl.Antecedent(np.arange(0, 3.1, 0.1),  'nivel_n')
    a = ctrl.Antecedent(np.arange(0, 5.1, 0.1),  'animo_n')

    # --- Consecuente ---
    i = ctrl.Consequent(np.arange(0, 10.1, 0.1), 'intensidad')

    # --- Membresías: horas ---
    h['baja']  = fuzz.trimf(h.universe, [0,  0,  5])
    h['media'] = fuzz.trimf(h.universe, [3,  7, 12])
    h['alta']  = fuzz.trimf(h.universe, [9, 20, 20])

    # --- Membresías: nivel ---
    n['principiante'] = fuzz.trimf(n.universe, [0.0, 0.0, 1.0])
    n['intermedio']   = fuzz.trimf(n.universe, [0.5, 1.0, 1.5])
    n['avanzado']     = fuzz.trimf(n.universe, [1.0, 2.0, 2.0])

    # --- Membresías: ánimo ---
    a['bajo']  = fuzz.trimf(a.universe, [0, 0, 2])
    a['medio'] = fuzz.trimf(a.universe, [1, 2, 3])
    a['alto']  = fuzz.trimf(a.universe, [2, 4, 4])

    # --- Membresías: intensidad ---
    i['baja']  = fuzz.trimf(i.universe, [0, 0, 4])
    i['media'] = fuzz.trimf(i.universe, [3, 5, 7])
    i['alta']  = fuzz.trimf(i.universe, [6, 10, 10])

    # --- Reglas ---
    reglas = [
        ctrl.Rule(a['bajo'],                                        i['baja']),   # R1
        ctrl.Rule(h['baja'],                                        i['baja']),   # R2
        ctrl.Rule(n['principiante'] & a['medio'],                   i['baja']),   # R3
        ctrl.Rule(n['principiante'] & a['alto'],                    i['media']),  # R4
        ctrl.Rule(n['intermedio']   & a['medio'],                   i['media']),  # R5
        ctrl.Rule(n['intermedio']   & a['alto'] & h['media'],       i['media']),  # R6
        ctrl.Rule(n['intermedio']   & a['alto'] & h['alta'],        i['alta']),   # R7
        ctrl.Rule(n['avanzado']     & a['medio'],                   i['media']),  # R8
        ctrl.Rule(n['avanzado']     & a['alto'] & h['media'],       i['media']),  # R9
        ctrl.Rule(n['avanzado']     & a['alto'] & h['alta'],        i['alta']),   # R10
    ]

    return ctrl.ControlSystem(reglas)


# Instancia global del sistema (se construye una sola vez)
_SISTEMA = _construir_sistema()


# ---------------------------------------------------------------------------
# Función pública
# ---------------------------------------------------------------------------

def determinar_intensidad(animo: str, horas: int, nivel: str) -> str:
    """
    Aplica el sistema difuso y devuelve 'baja', 'media' o 'alta'.

    Parámetros
    ----------
    animo  : str  — "Desanimado" | "Cansado" | "Normal" | "Bien" | "Excelente"
    horas  : int  — horas de entrenamiento por semana (1–20)
    nivel  : str  — "Principiante" | "Intermedio" | "Avanzado"
    """
    nivel_num = NIVEL_MAP.get(nivel, 1.0)
    animo_num = ANIMO_MAP.get(animo, 2.0)
    horas_num = float(max(0, min(20, horas)))

    sim = ctrl.ControlSystemSimulation(_SISTEMA)
    sim.input['horas']   = horas_num
    sim.input['nivel_n'] = nivel_num
    sim.input['animo_n'] = animo_num
    sim.compute()

    valor = sim.output['intensidad']

    if valor < 4.0:
        return "baja"
    elif valor > 6.0:
        return "alta"
    else:
        return "media"