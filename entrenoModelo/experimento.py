"""
experimento_neurofit.py
-----------------------
Recolecta datos de experimentación para NeuroFit:
  - Parámetros comparados
  - Convergencia (loss/accuracy por época)
  - Precisión final (accuracy, F1)
  - Tiempo de ejecución

Genera: resultados_experimento.json  (para visualización posterior)
"""

import time
import json
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Input

# ── Reproducibilidad ────────────────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# ── Dataset inline (mismo dataset_generator.py) ──────────────────────────────
OBJETIVOS = {"Perder peso": 0, "Ganar músculo": 1, "Resistencia": 2, "Tonificación": 3}
ANIMO     = {"Desanimado": 0, "Cansado": 1, "Normal": 2, "Bien": 3, "Excelente": 4}

def calcular_nivel(edad, peso, altura, horas, objetivo):
    score = 0
    if horas >= 6:   score += 2
    elif horas >= 3: score += 1
    if 18 <= edad <= 35: score += 1
    imc = peso / (altura / 100) ** 2
    if 20 <= imc <= 27: score += 1
    if objetivo == 1: score += 1
    if score <= 1:   return 0
    elif score <= 3: return 1
    else:            return 2

def generar_dataset(n=5000):
    rows = []
    for _ in range(n):
        edad    = random.randint(15, 70)
        peso    = random.randint(45, 120)
        altura  = random.randint(150, 200)
        horas   = random.randint(1, 10)
        obj     = random.randint(0, 3)
        animo   = random.randint(0, 4)
        nivel   = calcular_nivel(edad, peso, altura, horas, obj)
        rows.append([edad, peso, altura, horas, obj, animo, nivel])
    cols = ["edad","peso","altura","horas","objetivo","animo","nivel"]
    return pd.DataFrame(rows, columns=cols)

# ── Preparar datos ────────────────────────────────────────────────────────────
print("Generando dataset...")
df = generar_dataset(5000)

X = df[["edad","peso","altura","horas","objetivo","animo"]].values
y = df["nivel"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED
)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── Experimentos a comparar ───────────────────────────────────────────────────
EXPERIMENTOS = [
    {
        "nombre":     "Baseline (16-8)",
        "capas":      [16, 8],
        "dropout":    0.0,
        "epochs":     30,
        "batch_size": 32,
        "optimizer":  "adam",
    },
    {
        "nombre":     "Más neuronas (64-32)",
        "capas":      [64, 32],
        "dropout":    0.0,
        "epochs":     30,
        "batch_size": 32,
        "optimizer":  "adam",
    },
    {
        "nombre":     "Con Dropout (64-32-drop)",
        "capas":      [64, 32],
        "dropout":    0.3,
        "epochs":     30,
        "batch_size": 32,
        "optimizer":  "adam",
    },
    {
        "nombre":     "Batch pequeño (16-8, bs=16)",
        "capas":      [16, 8],
        "dropout":    0.0,
        "epochs":     30,
        "batch_size": 16,
        "optimizer":  "adam",
    },
    {
        "nombre":     "Más épocas (16-8, ep=60)",
        "capas":      [16, 8],
        "dropout":    0.0,
        "epochs":     60,
        "batch_size": 32,
        "optimizer":  "adam",
    },
    {
        "nombre":     "SGD optimizer (16-8)",
        "capas":      [16, 8],
        "dropout":    0.0,
        "epochs":     30,
        "batch_size": 32,
        "optimizer":  "sgd",
    },
]

# ── Función de construcción de modelo ─────────────────────────────────────────
def construir_modelo(capas, dropout, optimizer):
    layers = [Input(shape=(6,))]
    model_layers = []
    for n in capas:
        model_layers.append(Dense(n, activation="relu"))
        if dropout > 0:
            model_layers.append(Dropout(dropout))
    model_layers.append(Dense(3, activation="softmax"))

    model = Sequential(model_layers)
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

# ── Ejecutar experimentos ─────────────────────────────────────────────────────
resultados = []

y_train_cat = to_categorical(y_train, num_classes=3)
y_test_cat  = to_categorical(y_test,  num_classes=3)

for exp in EXPERIMENTOS:
    print(f"\n{'='*55}")
    print(f"  Experimento: {exp['nombre']}")
    print(f"{'='*55}")

    tf.random.set_seed(SEED)
    np.random.seed(SEED)

    model = construir_modelo(exp["capas"], exp["dropout"], exp["optimizer"])

    # Contar parámetros (build primero con input shape)
    model.build(input_shape=(None, 6))
    total_params = model.count_params()

    # Medir tiempo
    t_inicio = time.time()

    history = model.fit(
        X_train_sc, y_train_cat,
        validation_data=(X_test_sc, y_test_cat),
        epochs=exp["epochs"],
        batch_size=exp["batch_size"],
        verbose=0
    )

    t_fin = time.time()
    tiempo_seg = round(t_fin - t_inicio, 3)

    # Evaluar
    _, accuracy = model.evaluate(X_test_sc, y_test_cat, verbose=0)
    y_pred_raw  = model.predict(X_test_sc, verbose=0)
    y_pred      = np.argmax(y_pred_raw, axis=1)
    f1_macro    = f1_score(y_test, y_pred, average="macro")
    f1_weighted = f1_score(y_test, y_pred, average="weighted")

    print(f"  Accuracy : {accuracy:.4f}")
    print(f"  F1 macro : {f1_macro:.4f}")
    print(f"  Tiempo   : {tiempo_seg}s")
    print(f"  Parámetros: {total_params}")

    resultados.append({
        "nombre":      exp["nombre"],
        # Parámetros del experimento
        "params": {
            "capas":       exp["capas"],
            "dropout":     exp["dropout"],
            "epochs":      exp["epochs"],
            "batch_size":  exp["batch_size"],
            "optimizer":   exp["optimizer"],
            "total_params_modelo": total_params,
        },
        # Convergencia (por época)
        "convergencia": {
            "train_loss":  [round(v, 5) for v in history.history["loss"]],
            "val_loss":    [round(v, 5) for v in history.history["val_loss"]],
            "train_acc":   [round(v, 5) for v in history.history["accuracy"]],
            "val_acc":     [round(v, 5) for v in history.history["val_accuracy"]],
            "epocas":      list(range(1, len(history.history["loss"]) + 1)),
        },
        # Precisión final
        "precision": {
            "accuracy":     round(float(accuracy), 4),
            "f1_macro":     round(float(f1_macro), 4),
            "f1_weighted":  round(float(f1_weighted), 4),
            "loss_final":   round(float(history.history["val_loss"][-1]), 5),
        },
        # Tiempo de ejecución
        "tiempo": {
            "total_seg":      tiempo_seg,
            "seg_por_epoca":  round(tiempo_seg / exp["epochs"], 4),
        }
    })

# ── Guardar JSON ───────────────────────────────────────────────────────────────
OUTPUT = "./entrenoModelo/data/experimento/resultados_experimento.json"
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(f"\n✅ Resultados guardados en: {OUTPUT}")
print(f"   Total experimentos: {len(resultados)}")

# ── Resumen en tabla ───────────────────────────────────────────────────────────
print("\n" + "="*80)
print(f"{'EXPERIMENTO':<30} {'PARAMS':>8} {'ACC':>7} {'F1':>7} {'TIEMPO':>8} {'ÉPOCAS':>7}")
print("-"*80)
for r in resultados:
    print(
        f"{r['nombre']:<30}"
        f"{r['params']['total_params_modelo']:>8}"
        f"{r['precision']['accuracy']:>7.4f}"
        f"{r['precision']['f1_macro']:>7.4f}"
        f"{r['tiempo']['total_seg']:>8.2f}s"
        f"{r['params']['epochs']:>7}"
    )
print("="*80)