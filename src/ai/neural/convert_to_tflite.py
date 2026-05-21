# convert_to_tflite.py
import tensorflow as tf

model = tf.keras.models.load_model("data/models/neurofit_model.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("data/models/neurofit_model.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo convertido correctamente")