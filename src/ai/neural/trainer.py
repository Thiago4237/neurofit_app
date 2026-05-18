import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Input

from src.ai.neural.preprocess import (
    cargar_dataset,
    preparar_datos,
    guardar_scaler
)


DATASET_PATH = "data/training/neurofit_dataset.csv"
MODEL_PATH = "data/models/neurofit_model.keras"
SCALER_PATH = "data/models/scaler.pkl"

def construir_modelo(input_size):

    model = Sequential([

        Input(shape=(input_size,)),

        Dense(
            16,
            activation='relu'
        ),

        Dense(
            8,
            activation='relu'
        ),

        Dense(
            3,
            activation='softmax'
        )
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def main():

    print("Cargando dataset...")

    x, y = cargar_dataset(DATASET_PATH)

    (
        x_train,
        x_test,
        y_train,
        y_test,
        scaler
    ) = preparar_datos(x, y)

    y_train = to_categorical(y_train, num_classes=3)
    y_test = to_categorical(y_test, num_classes=3)

    print("Construyendo modelo...")

    model = construir_modelo(x_train.shape[1])

    print("Entrenando modelo...")

    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_test, y_test),
        epochs=30,
        batch_size=32,
        verbose=1
    )

    loss, accuracy = model.evaluate(x_test, y_test)

    print(f"Accuracy final: {accuracy:.4f}")

    model.save(MODEL_PATH)

    guardar_scaler(
        scaler,
        SCALER_PATH
    )

    print(f"Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    main()