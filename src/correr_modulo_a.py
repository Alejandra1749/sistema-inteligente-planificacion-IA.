import csv
from src.escenario import cargar_escenario
from src.busqueda_heuristica import greedy, astar

escenarios = ["config/escenario_01.json",
              "config/escenario_02.json",
              "config/escenario_03.json"]

algoritmos = [("Greedy", greedy), ("A*", astar)]

filas = []
for archivo in escenarios:
    esc = cargar_escenario(archivo)
    for nombre, algoritmo in algoritmos:
        r = algoritmo(esc, esc["inicio"], esc["destino"])
        filas.append([esc["nombre"], nombre, r["resultado"], r["costo"],
                      len(r["ruta"]), r["expandidos"],
                      round(r["tiempo_ms"], 3), r["ruta"]])
        print(esc["nombre"], nombre, "costo", r["costo"], "expandidos", r["expandidos"])

with open("resultados/modulo_a.csv", "w", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(["escenario", "algoritmo", "resultado", "costo",
                       "casillas_en_ruta", "expandidos", "tiempo_ms", "ruta"])
    escritor.writerows(filas)