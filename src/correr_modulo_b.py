import csv
import random
import statistics
from itertools import permutations
from src.escenario import cargar_escenario
from src.busqueda_local import calcular_matriz, costo_orden, hill_climbing, vecinos_swap

esc = cargar_escenario("config/escenario_04.json")
matriz = calcular_matriz(esc)

N = 15 # soluciones iniciales

filas = [] # lo que va al CSV
finales = [] # costo final de cada corrida
ordenes_finales = [] # órdenes finales distintos
con_meseta = 0

for i in range(N):
    semilla = esc["semilla"] + i
    random.seed(semilla)
    orden = esc["entregas"][:]
    random.shuffle(orden) # orden inicial 

    costo_ini = costo_orden(esc, matriz, orden)
    r = hill_climbing(esc, matriz, orden)

    # meseta
    iguales = 0
    for v in vecinos_swap(r["orden"]):
        if costo_orden(esc, matriz, v) == r["costo"]:
            iguales += 1
    if iguales > 0:
        con_meseta += 1

    finales.append(r["costo"])
    if r["orden"] not in ordenes_finales:
        ordenes_finales.append(r["orden"])

    filas.append([i + 1, semilla, orden, costo_ini, r["orden"], r["costo"],
                  r["pasos"], r["evaluaciones"], round(r["tiempo_ms"], 3), iguales])

# guardar en CSV
with open("resultados/modulo_b.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ejecucion", "semilla", "orden_inicial", "costo_inicial",
                "orden_final", "costo_final", "pasos", "evaluaciones",
                "tiempo_ms", "vecinos_con_mismo_costo"])
    w.writerows(filas)

# análisis
print("Costos finales:", sorted(finales))
print("Mejor:", min(finales), " Peor:", max(finales))
print("Promedio:", round(statistics.mean(finales), 2))
print("Desviación estándar:", round(statistics.stdev(finales), 2))
print("Órdenes finales distintos (óptimos locales):", len(ordenes_finales))
print("Veces que llegó al mejor costo:", finales.count(min(finales)), "de", N)
print("Corridas que terminaron en meseta:", con_meseta)

# óptimo real
mejor_real = None
for p in permutations(esc["entregas"]):
    c = costo_orden(esc, matriz, p)
    if mejor_real is None or c < mejor_real:
        mejor_real = c
print("Óptimo global (todas las permutaciones):", mejor_real)