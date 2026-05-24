# Aplicación móvil NeuroFit

## Descripción general

NeuroFit es una aplicación móvil desarrollada con:
- Python
- Kivy
- KivyMD

La aplicación utiliza un motor de inteligencia artificial integrado para:
- analizar información básica del usuario
- calcular intensidad de entrenamiento
- generar rutinas personalizadas
- adaptar ejercicios según objetivos y estado de ánimo

El proyecto está estructurado de forma modular para facilitar:
- mantenimiento
- escalabilidad
- entrenamiento de nuevos modelos
- actualización de rutinas
- compilación Android

---

# Estructura general del proyecto

```txt
appMovil/
   └── data/
      └── models/
   └── src/
      ├── ai/
      ├── core/
      ├── kvs/
      └── utils/
   ├── main.py
   ├── buildozer.spec
   └── requirements.txt
```

---

# 1. Archivo principal de entrada

Archivo:

```txt
main.py
```

## Función

Es el punto de entrada principal de la aplicación.

Desde este archivo:
- se inicia Kivy
- se carga la aplicación
- se ejecuta la app principal

## Ejecución local

```bash
python main.py
```

---

# 2. Carpeta data

Ruta:

```txt
data/
```

## Función

Contiene:
- modelos entrenados en la carpeta de models
- datos persistentes del usuario

---

## Carpeta models

Ruta:

```txt
data/models/
```

## Función

Aquí se almacenan los modelos utilizados por el motor de IA.

Los archivos deben copiarse desde el proyecto de entrenamiento.

## Archivos esperados

```txt
modelo.keras
modelo.tflite
scaler.pkl
config.json
```

## Importante

Sin estos archivos:
- el motor de IA no podrá cargar
- no se podrán generar rutinas
- la aplicación mostrará errores de inferencia

---

## Persistencia de usuario

La carpeta `data` también almacena la información básica del usuario.

Ejemplo:

```txt
user_data.json
```

## Datos almacenados

- edad
- peso
- altura
- horas disponibles


Esta información permite:
- mantener configuraciones entre sesiones
- evitar solicitar datos continuamente

---

# 3. Carpeta kvs

Ruta:

```txt
src/kvs/
```

## Función

Contiene los archivos `.kv` utilizados para las interfaces visuales.

Ejemplo:

```txt
welcome.kv
form.kv
dashboard.kv
```

---

## ¿Por qué separar los KV?

Mantener las interfaces separadas del código Python permite:
- mejor organización
- mantenimiento más sencillo
- menor complejidad
- separación entre lógica y diseño visual

Si toda la interfaz estuviera dentro de Python:
- el código sería mucho más complejo
- la depuración sería más difícil
- el mantenimiento sería menos escalable

---

# 4. Carpeta AI

Ruta:

```txt
src/ai/
```

## Función

Contiene todo el motor de inteligencia artificial utilizado por la aplicación.

---

# Carpeta neural

Ruta:

```txt
src/ai/neural/
```

## Función

Contiene el predictor basado en redes neuronales.

Archivo principal:

```txt
predictor.py
```

## Qué hace

Este archivo:
- carga el modelo entrenado
- carga el scaler
- prepara datos de entrada
- ejecuta inferencia
- devuelve predicciones

La inferencia principal utiliza:
- TensorFlow Lite (`.tflite`)
- NumPy

Esto permite:
- mejor rendimiento móvil
- menor consumo de memoria
- tiempos de respuesta rápidos

---

# Carpeta fuzzy

Ruta:

```txt
src/ai/fuzzy/
```

## Función

Implementa lógica difusa usando reglas de tipo Mamdani.

## Qué hace

Calcula el nivel de intensidad del entrenamiento según:
- objetivo del usuario
- nivel detectado
- estado de ánimo

Actualmente se manejan aproximadamente:
- 10 reglas difusas

Esto permite:
- recomendaciones más naturales
- mejor adaptación al usuario
- comportamiento menos rígido

---

# Base de rutinas

La aplicación incluye una base interna de ejercicios y rutinas.

## Función

Sirve como:
- fuente principal de ejercicios
- catálogo base de entrenamiento

La base puede:
- crecer con el tiempo
- recibir nuevos ejercicios
- agregar nuevas rutinas
- ampliar categorías

---

# Engine principal

Archivo:

```txt
engine.py
```

## Función

Centraliza toda la lógica del motor de IA.

Se encarga de:
- coordinar modelos
- ejecutar inferencias
- combinar reglas fuzzy
- generar rutinas finales
- organizar datos para la interfaz

Es el núcleo del sistema inteligente.

---

# 5. Carpeta utils

Ruta:

```txt
src/utils/
```

## Función

Contiene componentes auxiliares de la aplicación.

Principalmente:
- popups
- mensajes informativos
- ayudas visuales

---

## Objetivo

Mejorar la experiencia de usuario mostrando:
- errores
- advertencias
- confirmaciones
- información contextual

---

# 6. Carpeta core

Ruta:

```txt
src/core/
```

## Función

Es el corazón funcional de la aplicación.

Aquí se organiza:
- navegación
- carga de pantallas
- lógica principal
- conexión entre UI y motor IA

---

# Archivo screens.py

Relaciona:
- pantallas
- ScreenManager
- navegación entre vistas

---

# Archivo principal app.py

Contiene:
- lógica principal
- carga de pantallas
- carga de datos
- persistencia
- ejecución de rutinas
- renderizado dinámico

Es el archivo principal del comportamiento general de la aplicación.

---

# 7. Compilación Android

La aplicación se compila utilizando:

```txt
Buildozer
```

## Función

Buildozer permite:
- empaquetar aplicaciones Kivy
- generar APK Android
- gestionar dependencias
- automatizar compilación

---

# Archivo de configuración

Archivo:

```txt
buildozer.spec
```

## Qué contiene

- nombre del paquete
- dependencias
- permisos
- configuraciones Android
- API Android
- NDK y SDK
- assets incluidos
- arquitecturas soportadas

---

# Generar APK

## Compilar

```bash
buildozer android debug
```

## Compilar e instalar

```bash
buildozer android debug deploy run
```

---

# Importante

Antes de compilar verificar:
- SDK instalado
- NDK instalado
- dependencias correctas
- rutas válidas
- archivos `.kv`
- modelos en `data/models`

---

# Configuración preparada

El archivo `buildozer.spec` se deja configurado con:
- parámetros mínimos necesarios
- configuración Android funcional
- soporte para compilación rápida

En algunos casos puede ser necesario:
- comentar rutas
- reinstalar SDK/NDK
- limpiar Buildozer

Ejemplo:

```bash
buildozer android clean
```

---

# 8. Librerías

Archivo:

```txt
requirements.txt
```

## Función

Contiene las librerías necesarias para el desarrollo y funcionamiento de la aplicación.

Ejemplo:

```txt
Kivy
KivyMD
numpy
tflite-runtime
```

---

# Importancia

Mantener este archivo actualizado permite:
- evitar incompatibilidades
- facilitar despliegues
- mejorar mantenimiento
- reproducir entornos fácilmente

---

# Flujo general de funcionamiento

```txt
Usuario
   ↓
Formulario
   ↓
Carga de datos
   ↓
Modelo IA
   ↓
Sistema fuzzy
   ↓
Generación de rutina
   ↓
Renderizado en interfaz
```

---

# Recomendaciones

## Android

- usar `dp()` en tamaños
- evitar tamaños fijos
- usar `ScrollView`
- mantener layouts responsivos

---

## Modelos

- usar `.tflite` para producción móvil
- validar rutas antes de compilar
- mantener sincronizados los modelos

---

## Compilación

- evitar `clean` innecesarios
- usar builds incrementales
- probar siempre en dispositivo físico

---

# Tecnologías utilizadas

- Python
- Kivy
- KivyMD
- TensorFlow Lite
- NumPy
- lógica difusa Mamdani
- Buildozer
- Android SDK
- Android NDK
