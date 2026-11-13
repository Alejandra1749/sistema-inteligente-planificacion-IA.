import pandas as pd

datos = pd.read_csv("resultados/modulo_c.csv")
gen = datos[datos["metodo"] == "Genetico"]

optimo = 59         

print("Genético: costo final y generación de la última mejora")
print(gen[["ejecucion", "costo", "generacion_ultima_mejora"]].to_string(index=False))
print()

bien = gen[gen["costo"] == optimo]
mal = gen[gen["costo"] > optimo]

print("Corridas que llegaron al óptimo:", len(bien))
print("  generación promedio de su última mejora:",
      round(bien["generacion_ultima_mejora"].mean(), 1))
print("Corridas que NO llegaron:", len(mal))
print("  generación promedio de su última mejora:",
      round(mal["generacion_ultima_mejora"].mean(), 1))