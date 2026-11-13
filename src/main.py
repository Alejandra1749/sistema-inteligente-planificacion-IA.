
import json
import random
from src.escenario import cargar_escenario
from src.busqueda_heuristica import astar
from src.busqueda_local import calcular_matriz, hill_climbing
from src.metaheuristicas import recocido
from src.teoria_juegos import construir_matriz, equilibrios_nash
from src.adversaria import (calcular_valores, estado_inicial, aplicar,
                            es_terminal, acciones, minimax, mejor_jugada)

esc = cargar_escenario("config/escenario_04.json")
random.seed(esc["semilla"])
print("Escenario:", esc["nombre"], "- semilla", esc["semilla"])

#A*: costo real entre los puntos
matriz = calcular_matriz(esc)

# Teoría de juegos
juego = construir_matriz(esc)
nash = equilibrios_nash(juego)
reservo, reserva_otro = 2, 2
for k1, k2 in nash:
    if k1 == k2:                       
        reservo, reserva_otro = k1, k2
precio = esc["recursos"]["costo_transporte"]
if reservo + reserva_otro > esc["recursos"]["transporte"]:
    precio = precio * esc["competidor"]["factor"]    
costo_vehiculos = reservo * precio
print("Equilibrios de Nash:", nash)
print("Reservo", reservo, "vehículos a", precio, "cada uno =", costo_vehiculos)

# Minimax
valores = calcular_valores(esc, matriz)
PROF = 4
estado = estado_inicial(esc)
mias = []
del_competidor = []
while not es_terminal(estado):
    if estado[3] == 0:# turno MAX
        entrega, valor = mejor_jugada(estado, valores, PROF)
        mias.append(entrega)
    else:# turno MIN
        entrega = None
        menor = 1000
        for a in acciones(estado):
            v = minimax(aplicar(estado, a, valores), valores, PROF - 1, [0])
            if v < menor:
                menor = v
                entrega = a
        del_competidor.append(entrega)
    estado = aplicar(estado, entrega, valores)
print("Mis entregas:", mias)
print("Entregas del competidor:", del_competidor)

# Hill Climbing y recocido
mejor_orden = None
mejor_costo = None
for i in range(10):
    orden = mias[:]
    random.shuffle(orden)
    for r in [hill_climbing(esc, matriz, orden), recocido(esc, matriz, orden)]:
        if mejor_costo is None or r["costo"] < mejor_costo:
            mejor_costo = r["costo"]
            mejor_orden = r["orden"]
print("Mejor orden de visita:", mejor_orden, "- costo", mejor_costo)

# A* ruta completa 
puntos = [esc["inicio"]] + mejor_orden + [esc["destino"]]
ruta = [puntos[0]]
for a, b in zip(puntos, puntos[1:]):
    ruta = ruta + astar(esc, a, b)["ruta"][1:]

plan = {"escenario": esc["nombre"],
        "semilla": esc["semilla"],
        "vehiculos_reservados": reservo,
        "precio_por_vehiculo": precio,
        "costo_vehiculos": costo_vehiculos,
        "entregas_mias": mias,
        "entregas_competidor": del_competidor,
        "orden_visita": mejor_orden,
        "costo_ruta": mejor_costo,
        "casillas_en_ruta": len(ruta),
        "costo_total_plan": mejor_costo + costo_vehiculos,
        "ruta": ruta}

with open("resultados/plan_final.json", "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2)

print()
print("Costo de la ruta:", mejor_costo)
print("Costo de los vehículos:", costo_vehiculos)
print("Costo total del plan:", plan["costo_total_plan"])
print("Plan guardado en resultados/plan_final.json")