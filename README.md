# NeuroFit

## Descripción general

NeuroFit es una aplicación móvil enfocada en la generación de rutinas de entrenamiento personalizadas utilizando inteligencia artificial.

La aplicación analiza información básica del usuario como:
- edad
- peso
- altura
- tiempo disponible
- objetivo de entrenamiento
- estado de ánimo

Con esta información el sistema:
- calcula un nivel de entrenamiento
- determina una intensidad adecuada
- genera una rutina personalizada
- adapta los ejercicios según el perfil del usuario

---

# Objetivo del proyecto

El objetivo principal de NeuroFit es ofrecer una experiencia de entrenamiento:
- personalizada
- adaptable
- ligera
- funcional en dispositivos móviles

La aplicación utiliza:
- modelos de inteligencia artificial
- lógica difusa
- inferencia optimizada con TensorFlow Lite

Todo esto permite generar recomendaciones rápidas directamente desde el dispositivo móvil.

---

# Estructura principal del proyecto

El proyecto está dividido en dos partes principales:

```txt
Proyecto/
├── appMovil/
└── entrenoModelo/
```

---

# Carpeta appMovil

Ruta:

```txt
appMovil/
```

## Función

Contiene toda la aplicación móvil desarrollada con:
- Python
- Kivy
- KivyMD

Aquí se encuentra:
- interfaz gráfica
- lógica principal
- motor de IA integrado
- modelos utilizados por la aplicación
- sistema de generación de rutinas
- configuración de compilación Android

---

## Incluye

- pantallas visuales
- lógica de navegación
- inferencia con TensorFlow Lite
- persistencia de usuario
- integración fuzzy
- compilación Android con Buildozer

---

## Compilación

La aplicación Android se genera utilizando:

```txt
Buildozer
```

El APK final se instala directamente en dispositivos Android.

---

# Carpeta entrenoModelo

Ruta:

```txt
entrenoModelo/
```

## Función

Contiene toda la lógica relacionada con:
- generación de datasets
- entrenamiento de modelos
- experimentación
- pruebas
- conversión a TensorFlow Lite

---

## Incluye

- generación de datos sintéticos
- preprocesamiento
- entrenamiento del modelo
- pruebas de configuración
- evaluación de resultados
- exportación de modelos

---

## Resultado final

El proceso de entrenamiento genera archivos como:

```txt
.keras
.tflite
.json
.pkl
```

Estos archivos posteriormente se copian al proyecto móvil para ser utilizados por el motor de IA integrado.

---

# Flujo general del sistema

```txt
Entrenamiento del modelo
        ↓
Generación de archivos IA
        ↓
Conversión a TensorFlow Lite
        ↓
Copia al proyecto móvil
        ↓
Integración en Android
        ↓
Generación de rutinas
```

---

# Tecnologías utilizadas

## Aplicación móvil

- Python
- Kivy
- KivyMD
- TensorFlow Lite
- NumPy

---

## Inteligencia artificial

- TensorFlow
- TensorFlow Lite
- lógica difusa Mamdani
- modelos de clasificación

---

## Compilación Android

- Buildozer
- Android SDK
- Android NDK
- Python-for-Android

---

# Funcionamiento general

El usuario ingresa sus datos básicos dentro de la aplicación.

Posteriormente:
1. el modelo neuronal analiza el perfil
2. el sistema fuzzy calcula intensidad
3. el motor organiza ejercicios
4. la aplicación genera la rutina final

Todo el procesamiento ocurre directamente en el dispositivo móvil utilizando inferencia optimizada.

---

# Características principales

- generación de rutinas personalizadas
- inferencia local sin conexión
- uso de TensorFlow Lite
- sistema fuzzy adaptable
- almacenamiento local de usuario
- arquitectura modular
- compilación Android nativa con Python

---

# Notas importantes

- Los modelos deben existir dentro de `appMovil/data/models`
- La aplicación depende de los modelos generados en `entrenoModelo`
- Se recomienda mantener sincronizados ambos proyectos
- El archivo `buildozer.spec` contiene la configuración principal de compilación Android

---

# Documentación adicional

Cada módulo principal posee su propio README:

## Entrenamiento de modelos

```txt
README_Entrenamiento_NeuroFit.md
```

## Aplicación móvil

```txt
README_App_Movil_NeuroFit.md
```
