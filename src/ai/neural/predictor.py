import numpy as np
import tensorflow as tf
import pandas as pd

from src.ai.neural.preprocess import cargar_scaler


MODEL_PATH = "data/models/neurofit_model.keras"

SCALER_PATH = "data/models/scaler.pkl"


NIVELES = {
    0: "Principiante",
    1: "Intermedio",
    2: "Avanzado"
}


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


class NeuroFitPredictor:

    def __init__(self):

        print("Cargando modelo...")

        self.model = tf.keras.models.load_model(
            MODEL_PATH
        )

        print("Cargando scaler...")

        self.scaler = cargar_scaler(
            SCALER_PATH
        )

    def preparar_entrada(
        self,
        edad,
        peso,
        altura,
        horas,
        objetivo,
        animo
    ):

        objetivo_val = OBJETIVOS.get(objetivo, 0)
        animo_val = ANIMO.get(animo, 2)
        
        data = pd.DataFrame([{
            "edad": edad,
            "peso": peso,
            "altura": altura,
            "horas": horas,
            "objetivo": objetivo_val,
            "animo": animo_val
        }])

        data_scaled = self.scaler.transform(data)

        return data_scaled

    def predecir_nivel(
        self,
        edad,
        peso,
        altura,
        horas,
        objetivo,
        animo
    ):

        entrada = self.preparar_entrada(
            edad,
            peso,
            altura,
            horas,
            objetivo,
            animo
        )

        prediction = self.model.predict(
            entrada,
            verbose=0
        )

        nivel_idx = np.argmax(prediction)

        confianza = float(np.max(prediction))

        return {
            "nivel": NIVELES[nivel_idx],
            "confianza": round(confianza, 4),
            "raw_prediction": prediction.tolist()
        }


if __name__ == "__main__":

    predictor = NeuroFitPredictor()

    resultado = predictor.predecir_nivel(
        edad=24,
        peso=72,
        altura=175,
        horas=5,
        objetivo="Ganar músculo",
        animo="Bien"
    )

    print(resultado)