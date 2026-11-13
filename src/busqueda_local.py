# búsqueda local
import time
from src.escenario import puntos_clave
from src.busqueda_heuristica import astar


def calcular_matriz(esc):
    #costo real de ir de un punto a otro
    puntos = puntos_clave(esc)
    matriz = {}
    for a in puntos:
        for b in puntos:
            if a != b:
                matriz[(a, b)] = astar(esc, a, b)["costo"]
    return matriz


def costo_orden(esc, matriz, orden):
    total = 0
    actual = esc["inicio"]
    for entrega in orden:
        total += matriz[(actual, entrega)]
        actual = entrega
    total += matriz[(actual, esc["destino"])]
    return total


#############hill_climbing#################

def vecinos_swap(orden):
    #ordenes que salen
    lista = []
    for i in range(len(orden)):
        for j in range(i + 1, len(orden)):
            nuevo = orden[:] # copia
            nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
            lista.append(nuevo)
    return lista


def hill_climbing(esc, matriz, orden_inicial):
    t0 = time.perf_counter()
    actual = orden_inicial[:]
    costo_actual = costo_orden(esc, matriz, actual)
    evaluaciones = 1
    pasos = 0

    while True:
        mejor = None
        mejor_costo = costo_actual
        for v in vecinos_swap(actual):
            c = costo_orden(esc, matriz, v)
            evaluaciones += 1
            if c < mejor_costo:#se queda con los que mejora
                mejor = v
                mejor_costo = c

        if mejor is None:#si ningun vecino mejora se detiene 
            break

        actual = mejor
        costo_actual = mejor_costo
        pasos += 1

    return {"orden": actual,
            "costo": costo_actual,
            "pasos": pasos,
            "evaluaciones": evaluaciones,
            "tiempo_ms": (time.perf_counter() - t0) * 1000}