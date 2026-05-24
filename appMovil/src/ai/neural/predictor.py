import json
import numpy as np
import os
from kivy.resources import resource_find

try:
    import tflite_runtime.interpreter as tflite
    Interpreter = tflite.Interpreter
except ImportError:
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter


MODEL_PATH = resource_find("data/models/neurofit_model.tflite")
SCALER_PATH = resource_find("data/models/scaler.json")

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

        print("Cargando modelo TFLite...")

        self.interpreter = Interpreter(model_path=MODEL_PATH)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        print("Cargando scaler...")

        with open(SCALER_PATH, "r") as f:
            scaler_data = json.load(f)

        self.mean = np.array(scaler_data["mean"], dtype=np.float32)
        self.scale = np.array(scaler_data["scale"], dtype=np.float32)

    def preparar_entrada(
        self,
        edad,
        peso,
        altura,
        horas,
        objetivo,
        animo
    ):

        data = np.array([[
            edad,
            peso,
            altura,
            horas,
            OBJETIVOS.get(objetivo, 0),
            ANIMO.get(animo, 2)
        ]], dtype=np.float32)

        # StandardScaler manual
        scaled = (data - self.mean) / self.scale

        return scaled.astype(np.float32)

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

        self.interpreter.set_tensor(
            self.input_details[0]['index'],
            entrada
        )

        self.interpreter.invoke()

        prediction = self.interpreter.get_tensor(
            self.output_details[0]['index']
        )

        nivel_idx = int(np.argmax(prediction))
        confianza = float(np.max(prediction))

        return {
            "nivel": NIVELES[nivel_idx],
            "confianza": round(confianza, 4),
            "raw_prediction": prediction.tolist()
        }