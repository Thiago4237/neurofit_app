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
