import random
import pandas as pd


OBJETIVOS = {
    "Perder peso": 0,
    "Ganar músculo": 1,
    "Resistencia": 2,
    "Tonificación": 3
}

ANIMO = {
    "Desanimado": 0,
    "Cansado": 1,
    "Normal": 2,
    "Bien": 3,
    "Excelente": 4
}


def calcular_nivel(edad, peso, altura, horas, objetivo):
    """
    Genera una clasificación sintética:
    0 = principiante
    1 = intermedio
    2 = avanzado
    """

    score = 0

    # Horas de entrenamiento
    if horas >= 6:
        score += 2
    elif horas >= 3:
        score += 1

    # Edad
    if 18 <= edad <= 35:
        score += 1

    # IMC aproximado
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)

    if 20 <= imc <= 27:
        score += 1

    # Objetivo
    if objetivo == OBJETIVOS["Ganar músculo"]:
        score += 1

    # Clasificación final
    if score <= 1:
        return 0  # principiante
    elif score <= 3:
        return 1  # intermedio
    else:
        return 2  # avanzado


def generar_dataset(cantidad=5000):
    data = []

    for _ in range(cantidad):

        edad = random.randint(15, 70)
        peso = random.randint(45, 120)
        altura = random.randint(150, 200)
        horas = random.randint(1, 10)

        objetivo_nombre = random.choice(list(OBJETIVOS.keys()))
        animo_nombre = random.choice(list(ANIMO.keys()))

        objetivo = OBJETIVOS[objetivo_nombre]
        animo = ANIMO[animo_nombre]

        nivel = calcular_nivel(
            edad,
            peso,
            altura,
            horas,
            objetivo
        )

        data.append([
            edad,
            peso,
            altura,
            horas,
            objetivo,
            animo,
            nivel
        ])

    columns = [
        "edad",
        "peso",
        "altura",
        "horas",
        "objetivo",
        "animo",
        "nivel"
    ]

    return pd.DataFrame(data, columns=columns)


if __name__ == "__main__":

    df = generar_dataset(5000)

    print(df.head())

    df.to_csv("./entrenoModelo/data/training/neurofit_dataset.csv", index=False)

    print("Dataset generado correctamente")