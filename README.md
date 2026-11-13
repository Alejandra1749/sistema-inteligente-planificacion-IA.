# Sistema inteligente de planificación, optimización y toma de decisiones adversarias

Proyecto de Inteligencia Artificial que integra búsqueda heurística, búsqueda local, metaheurísticas, teoría de juegos y búsqueda adversaria para optimizar rutas de entrega y asignación de recursos frente a un competidor en entornos discretos.

## Estructura del repositorio

```text
proyecto_IA/
├── README.md
├── requirements.txt
├── config/
│   ├── escenario_01.json
│   ├── escenario_02.json
│   ├── escenario_03.json
│   ├── escenario_04.json
│   └── escenario_sin_solucion.json
├── src/
│   ├── __init__.py
│   ├── escenario.py
│   ├── busqueda_heuristica.py
│   ├── correr_modulo_a.py
│   ├── comparar_modulo_a.py
│   ├── busqueda_local.py
│   ├── correr_modulo_b.py
│   ├── metaheuristicas.py
│   ├── correr_modulo_c.py
│   ├── analisis_convergencia.py
│   ├── teoria_juegos.py
│   ├── adversaria.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── probar_escenarios.py
│   ├── probar_juego.py
│   └── probar_adversaria.py
├── resultados/
│   ├── modulo_a.csv
│   ├── modulo_a_comparacion.png
│   ├── modulo_b.csv
│   ├── modulo_c.csv
│   ├── modulo_c_comparacion.png
│   └── plan_final.json
├── informe/
│   └── Informe_Final_Proyecto_IA.pdf
└── venv/
```

## Requisitos e instalación

Para ejecutar el proyecto se necesita:

- Python 3.11 o una versión compatible.
- Las dependencias indicadas en `requirements.txt`.

### 1. Ubicarse en la carpeta del proyecto

```bash
cd proyecto_IA
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual en Windows

```bash
venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Las dependencias utilizadas son:

- matplotlib
- pandas
- numpy
- pytest

## Ejecución del proyecto

Todos los comandos deben ejecutarse desde la carpeta principal `proyecto_IA/`, con el entorno virtual activado.

### 1. Flujo principal integrado

Ejecuta la planificación completa utilizando el escenario `escenario_04.json`.

Durante la ejecución se calculan los costos de las rutas mediante A*, se determina la reserva de vehículos mediante teoría de juegos, se asignan las entregas mediante Minimax y se optimiza el orden de visita utilizando Hill Climbing y Recocido Simulado.

Al finalizar, se genera el archivo `resultados/plan_final.json`.

```bash
python -m src.main
```

### 2. Experimentos por módulo

**Módulo A. Búsqueda heurística: Greedy y A***

Ejecuta las búsquedas en los escenarios 01, 02 y 03. También realiza la comparación de costos, nodos expandidos y admisibilidad de la heurística, generando una gráfica.

```bash
python -m src.correr_modulo_a
python -m src.comparar_modulo_a
```

**Módulo B. Búsqueda local: Hill Climbing**

Ejecuta múltiples soluciones iniciales para encontrar un orden de visita de las entregas y genera los resultados de las corridas.

```bash
python -m src.correr_modulo_b
```

**Módulo C. Metaheurísticas: Recocido Simulado y Algoritmo Genético**

Ejecuta 20 corridas por cada método y compara sus resultados. También realiza el análisis de convergencia del Algoritmo Genético.

```bash
python -m src.correr_modulo_c
python -m src.analisis_convergencia
```

**Módulo D. Teoría de juegos**

Construye la matriz de pagos, identifica las mejores respuestas, analiza la dominancia de estrategias y calcula los equilibrios de Nash.

```bash
python -m tests.probar_juego
```

**Módulo E. Búsqueda adversaria: Minimax y Poda Alfa-Beta**

Ejecuta la búsqueda adversaria y compara los resultados de Minimax y Alfa-Beta, considerando nodos visitados, nodos podados y tiempos de ejecución.

```bash
python -m tests.probar_adversaria
```

## Pruebas y validación

El proyecto incluye archivos para revisar el funcionamiento de los escenarios y de los módulos de teoría de juegos y búsqueda adversaria.

**Validación de escenarios**

Comprueba que los escenarios puedan cargarse y detecta los casos en los que no existe una ruta posible hacia alguno de los puntos importantes.

```bash
python -m tests.probar_escenarios
```

**Pruebas de teoría de juegos**

```bash
python -m tests.probar_juego
```

**Pruebas de búsqueda adversaria**

```bash
python -m tests.probar_adversaria
```

## Archivos de resultados

Los resultados de los experimentos se guardan en la carpeta `resultados/`.

| Archivo | Descripción |
|---|---|
| `modulo_a.csv` | Resultados de las búsquedas Greedy y A*. |
| `modulo_a_comparacion.png` | Gráfica comparativa del Módulo A. |
| `modulo_b.csv` | Resultados de las corridas de Hill Climbing. |
| `modulo_c.csv` | Resultados de Recocido Simulado y Algoritmo Genético. |
| `modulo_c_comparacion.png` | Gráfica comparativa del Módulo C. |
| `plan_final.json` | Plan de entregas generado por el flujo principal integrado. |

## Configuración de escenarios

Los escenarios se encuentran en la carpeta `config/` y se almacenan en formato JSON.

- `escenario_01.json`, `escenario_02.json` y `escenario_03.json`: escenarios utilizados para comparar los algoritmos de búsqueda heurística.
- `escenario_04.json`: escenario utilizado para los experimentos de búsqueda local, metaheurísticas y el flujo principal integrado.
- `escenario_sin_solucion.json`: escenario utilizado para comprobar la detección de situaciones en las que no existe una ruta posible.

Cada escenario contiene información sobre el tamaño de la cuadrícula, inicio, destino, puntos de entrega, obstáculos, costos de movimiento, recursos disponibles, competidor y semilla aleatoria.

## Reproducibilidad

Los escenarios cuentan con semillas aleatorias para facilitar la repetición de los experimentos. Los parámetros de los algoritmos se encuentran definidos en sus respectivos archivos de Python.

Para repetir los experimentos, se deben ejecutar los comandos correspondientes desde la carpeta principal del proyecto.
```
