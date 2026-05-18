import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "edad",
    "peso",
    "altura",
    "horas",
    "objetivo",
    "animo"
]

TARGET_COLUMN = "nivel"


def cargar_dataset(path):

    df = pd.read_csv(path)

    x = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return x, y


def preparar_datos(x, y):

    scaler = StandardScaler()

    x_scaled = scaler.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(
        x_scaled,
        y,
        test_size=0.2,
        random_state=42
    )

    return (
        x_train,
        x_test,
        y_train,
        y_test,
        scaler
    )


def guardar_scaler(scaler, path):
    joblib.dump(scaler, path)
    print(f"Scaler guardado en: {path}")


def cargar_scaler(path):
    return joblib.load(path)