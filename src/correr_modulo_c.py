import csv
import random
import statistics
from itertools import permutations
import matplotlib.pyplot as plt
from src.escenario import cargar_escenario
from src.busqueda_local import calcular_matriz, costo_orden
from src.metaheuristicas import recocido, genetico

esc = cargar_escenario("config/escenario_04.json")
matriz = calcular_matriz(esc)

N = 20 # ejecuciones por método
res_recocido = []
res_genetico = []

for i in range(N):
    semilla = esc["semilla"] + i

    random.seed(semilla)
    orden = esc["entregas"][:]
    random.shuffle(orden)
    res_recocido.append(recocido(esc, matriz, orden))

    random.seed(semilla)
    res_genetico.append(genetico(esc, matriz))

# guardar en el CSV
with open("resultados/modulo_c.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["metodo", "ejecucion", "semilla", "orden_final", "costo",
                "evaluaciones", "tiempo_ms", "generacion_ultima_mejora"])
    for i in range(N):
        semilla = esc["semilla"] + i
        r = res_recocido[i]
        w.writerow(["Recocido", i + 1, semilla, r["orden"], r["costo"],
                    r["evaluaciones"], round(r["tiempo_ms"], 3), ""])

        r = res_genetico[i]
        h = r["historial"]
        ultima = 1 # generación donde llegó a su mejor costo
        for g in range(1, len(h)):
            if h[g] < h[g - 1]:
                ultima = g + 1
        w.writerow(["Genetico", i + 1, semilla, r["orden"], r["costo"],
                    r["evaluaciones"], round(r["tiempo_ms"], 3), ultima])

# óptimo real 
optimo = None
for p in permutations(esc["entregas"]):
    c = costo_orden(esc, matriz, p)
    if optimo is None or c < optimo:
        optimo = c
print("Óptimo global:", optimo)


def resumen(nombre, resultados):
    costos = [r["costo"] for r in resultados]
    print(nombre)
    print("  mejor costo:", min(costos))
    print("  peor costo:", max(costos))
    print("  promedio:", round(statistics.mean(costos), 2))
    print("  desviación estándar:", round(statistics.stdev(costos), 2))
    print("  llegó al óptimo:", costos.count(optimo), "de", N)
    print("  evaluaciones:", round(statistics.mean([r["evaluaciones"] for r in resultados])))
    print("  tiempo promedio (ms):", round(statistics.mean([r["tiempo_ms"] for r in resultados]), 2))


resumen("Recocido", res_recocido)
resumen("Genético", res_genetico)

# gráfica
plt.boxplot([[r["costo"] for r in res_recocido], [r["costo"] for r in res_genetico]])
plt.xticks([1, 2], ["Recocido", "Genético"])
plt.ylabel("Costo final")
plt.title("20 ejecuciones por método")
plt.savefig("resultados/modulo_c_comparacion.png")