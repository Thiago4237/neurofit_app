import random

from src.ai.routines.exercises import EXERCISES
from src.ai.routines.templates import ROUTINE_TEMPLATES
from src.ai.routines.intensity import INTENSITY_CONFIG


class RoutineGenerator:

    def __init__(self):
        pass

    def generar_rutina(
        self,
        nivel,
        intensidad="media"
    ):

        template = ROUTINE_TEMPLATES[nivel]
        grupos = template["ejercicios"]
        cantidad = template["cantidad"]
        config = INTENSITY_CONFIG[intensidad]

        rutina = []
        usados = set()

        while len(rutina) < cantidad:

            grupo = random.choice(grupos)

            ejercicio = random.choice(
                EXERCISES[grupo]
            )

            if ejercicio in usados:
                continue

            usados.add(ejercicio)

            rutina.append({
                "ejercicio": ejercicio,
                "series": config["series"],
                "repeticiones": config["repeticiones"],
                "descanso": config["descanso"]
            })

        return rutina


if __name__ == "__main__":

    generator = RoutineGenerator()

    rutina = generator.generar_rutina(
        nivel="Intermedio",
        intensidad="media"
    )

    print("\nRUTINA GENERADA\n")

    for idx, ejercicio in enumerate(rutina, start=1):

        print(
            f"{idx}. "
            f"{ejercicio['ejercicio']} - "
            f"{ejercicio['series']}x"
            f"{ejercicio['repeticiones']} "
            f"(Descanso {ejercicio['descanso']})"
        )