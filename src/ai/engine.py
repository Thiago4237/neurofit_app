from src.core.screens import WelcomeScreen, FormScreen, DashboardScreen
from src.ai.neural.predictor import NeuroFitPredictor
from src.ai.routines.routine_generator import RoutineGenerator
from src.ai.fuzzy.fuzzy_intensity import determinar_intensidad


class NeuroFitEngine:

    def __init__(self):
        print("Inicializando NeuroFit Engine...")
        self.predictor = NeuroFitPredictor()
        self.generator = RoutineGenerator()

    def generar_plan(
        self,
        edad,
        peso,
        altura,
        horas,
        objetivo,
        animo
    ):

        # -------------------------
        # Predicción neuronal
        # -------------------------

        prediccion = self.predictor.predecir_nivel(
            edad,
            peso,
            altura,
            horas,
            objetivo,
            animo
        )

        nivel = prediccion["nivel"]
        confianza = prediccion["confianza"]

        # -------------------------
        # Intensidad difusa
        # -------------------------

        intensidad = determinar_intensidad(
            animo=animo,
            horas=horas,
            nivel=nivel
        )

        # -------------------------
        # Generar rutina
        # -------------------------

        rutina = self.generator.generar_rutina(
            nivel=nivel,
            intensidad=intensidad
        )

        # -------------------------
        # Resultado final
        # -------------------------

        return {
            "nivel": nivel,
            "confianza": confianza,
            "intensidad": intensidad,
            "rutina": rutina
        }


if __name__ == "__main__":

    engine = NeuroFitEngine()

    resultado = engine.generar_plan(
        edad=24,
        peso=74,
        altura=178,
        horas=5,
        objetivo="Ganar músculo",
        animo="Bien"
    )

    print("\n=== NEUROFIT ===\n")

    print(f"Nivel: {resultado['nivel']}")
    print(f"Confianza: {resultado['confianza']}")
    print(f"Intensidad: {resultado['intensidad']}")

    print("\nRutina:\n")

    for idx, ejercicio in enumerate(
        resultado["rutina"],
        start=1
    ):
        print(
            f"{idx}. "
            f"{ejercicio['ejercicio']} - "
            f"{ejercicio['series']}x"
            f"{ejercicio['repeticiones']} "
            f"(Descanso {ejercicio['descanso']})"
        )