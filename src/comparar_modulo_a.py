import pandas as pd
import matplotlib.pyplot as plt
from src.escenario import cargar_escenario
from src.busqueda_heuristica import manhattan, astar

datos = pd.read_csv("resultados/modulo_a.csv")

costos = datos.pivot(index="escenario", columns="algoritmo", values="costo")
expandidos = datos.pivot(index="escenario", columns="algoritmo", values="expandidos")

print("Costo de la ruta")
print(costos)
print()
print("Nodos expandidos")
print(expandidos)
print()

# costo greedy vs A*
extra = (costos["Greedy"] - costos["A*"]) / costos["A*"] * 100
print("Greedy es más caro que A* en (%):")
print(extra.round(1))
print()

# comprobar la admisibilidad
print("ADMISIBILIDAD")
for nombre in ["01", "02", "03"]:
    esc = cargar_escenario("config/escenario_" + nombre + ".json")
    h = manhattan(esc["inicio"], esc["destino"])
    real = astar(esc, esc["inicio"], esc["destino"])["costo"]
    print("escenario_" + nombre, "h =", h, " costo real =", real, " cumple:", h <= real)

# gráficas
figura, ejes = plt.subplots(1, 2, figsize=(10, 4))
costos.plot(kind="bar", ax=ejes[0], title="Costo de la ruta")
expandidos.plot(kind="bar", ax=ejes[1], title="Nodos expandidos")
for eje in ejes:
    eje.set_xlabel("")
    eje.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig("resultados/modulo_a_comparacion.png")
print()
print("Gráfica guardada en resultados/modulo_a_comparacion.png")