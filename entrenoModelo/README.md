# Entrenamiento y generación de modelos NeuroFit

## Flujo general

El proceso completo para generar y actualizar los modelos utilizados por la aplicación móvil consta de las siguientes etapas:

1. Generar dataset sintético  
2. Verificar el preprocesamiento  
3. Ejecutar pruebas y experimentos  
4. Entrenar el modelo final  
5. Verificar archivos generados  
6. Convertir el modelo a TensorFlow Lite (`.tflite`)  
7. Copiar modelos al proyecto móvil  

---

# 1. Generar el dataset sintético

Archivo:

```txt
dataset_generator.py
```

Ubicación:

```txt
entrenoModelo/dataset_generator.py
```

## Qué hace

Genera el dataset sintético utilizado para entrenar el modelo de IA.

El archivo generado se guarda en:

```txt
data/training
```

## Antes de ejecutar

Verificar:
- rutas de guardado
- nombres de archivos
- permisos de escritura

## Ejecutar

```bash
python .\entrenoModelo\dataset_generator.py
```

---

# 2. Verificar el preprocesamiento

Archivo:

```txt
preprocess.py
```

## Qué hace

Contiene funciones auxiliares para:
- limpieza de datos
- normalización
- transformación de variables
- preparación del dataset

## Importante

Normalmente NO es necesario modificar este archivo.

Solo verificar:
- que las rutas existan
- que las funciones estén completas
- que no existan errores de importación

---

# 3. Ejecutar experimentos y pruebas

Archivo:

```txt
experimento.py
```

Ubicación:

```txt
entrenoModelo/experimento.py
```

## Qué hace

Ejecuta múltiples pruebas del modelo para:
- comparar configuraciones
- evaluar precisión
- probar hiperparámetros
- seleccionar la mejor arquitectura

## Resultado

Genera:
- comparativas en consola
- métricas de entrenamiento
- archivo JSON con resultados

El JSON se guarda en:

```txt
data/experimento
```

## Importante

Este archivo es auxiliar y normalmente NO requiere modificaciones.

## Ejecutar

```bash
python .\entrenoModelo\experimento.py
```

---

# 4. Entrenar el modelo final

Archivo:

```txt
trainer.py
```

Ubicación:

```txt
entrenoModelo/trainer.py
```

## Qué hace

Genera los archivos finales utilizados por la aplicación móvil.

Archivos generados:
- modelo `.keras`
- scaler `.pkl`
- configuraciones `.json`

## Salida

Los archivos se guardan en:

```txt
data/models
```

## Ejecutar

```bash
python .\entrenoModelo\trainer.py
```

---

# 5. Verificar archivos generados

Después del entrenamiento verificar que existan los archivos en:

```txt
data/models
```

## Archivos esperados

Ejemplo:

```txt
modelo.keras
scaler.pkl
config.json
```

La ubicación exacta depende de las rutas definidas dentro de:

```txt
trainer.py
```

---

# 6. Convertir el modelo a TensorFlow Lite

Archivo:

```txt
convert_to_tflite.py
```

Ubicación:

```txt
entrenoModelo/convert_to_tflite.py
```

## Qué hace

Convierte el modelo entrenado al formato:

```txt
.tflite
```

Este formato está optimizado para:
- Android
- aplicaciones móviles
- inferencia rápida
- menor consumo de memoria

## Salida

El archivo `.tflite` se guarda en:

```txt
data/models
```

## Ejecutar

```bash
python .\entrenoModelo\convert_to_tflite.py
```

---

# 7. Copiar modelos al proyecto móvil

En el proyecto móvil existe la carpeta:

```txt
data/models
```

## Copiar los siguientes archivos

Desde el proyecto de entrenamiento:

```txt
data/models
```

Hacia el proyecto móvil:

```txt
data/models
```

## Archivos necesarios

```txt
.keras
.tflite
.json
.pkl
```

## Importante

Estos archivos son necesarios para que la aplicación móvil pueda:
- cargar el modelo
- realizar inferencias
- calcular intensidad
- generar rutinas
- predecir nivel de entrenamiento

Sin estos archivos la aplicación NO podrá ejecutar el motor de IA.

---

# Estructura esperada

```txt
data/
├── training/
├── experimento/
└── models/
    ├── modelo.keras
    ├── modelo.tflite
    ├── scaler.pkl
    └── config.json
```

---

# Comandos rápidos

## Generar dataset

```bash
python .\entrenoModelo\dataset_generator.py
```

## Ejecutar experimentos

```bash
python .\entrenoModelo\experimento.py
```

## Entrenar modelo final

```bash
python .\entrenoModelo\trainer.py
```

## Convertir a TFLite

```bash
python .\entrenoModelo\convert_to_tflite.py
```
