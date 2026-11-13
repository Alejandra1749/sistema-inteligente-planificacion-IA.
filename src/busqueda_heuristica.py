import time
from src.escenario import vecinos, costo
 
#manhattan
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
 
#greedy
def greedy(esc, inicio, meta):
    t0 = time.perf_counter()
    frontera = [(manhattan(inicio, meta), inicio, [inicio], 0)]
    vistos = [inicio]
    expandidos = 0
 
    while len(frontera) > 0:
        frontera.sort()
        h, actual, ruta, gastado = frontera.pop(0)   
        expandidos += 1
 
        if actual == meta:
            return {"ruta": ruta,
                    "costo": gastado,
                    "expandidos": expandidos,
                    "tiempo_ms": (time.perf_counter() - t0) * 1000,
                    "resultado": "llegó a la meta"}
 
        for v in vecinos(esc, actual[0], actual[1]):
            if v not in vistos:
                vistos.append(v)
                frontera.append((manhattan(v, meta), v, ruta + [v],
                                 gastado + costo(esc, v[0], v[1])))
 
    return {"ruta": [], "costo": None,
            "expandidos": expandidos,
            "tiempo_ms": (time.perf_counter() - t0) * 1000,
            "resultado": "sin ruta"}
 
#A*
def astar(esc, inicio, meta):
    t0 = time.perf_counter()
 
    frontera = [(manhattan(inicio, meta), inicio, [inicio], 0)]
    visitados = []
    expandidos = 0
 
    while len(frontera) > 0:
        frontera.sort()
        f, actual, ruta, g = frontera.pop(0)   #f menor
 
        if actual in visitados:     #visitados
            continue
        visitados.append(actual)
        expandidos += 1
 
        if actual == meta:
            return {"ruta": ruta,
                    "costo": g,
                    "expandidos": expandidos,
                    "tiempo_ms": (time.perf_counter() - t0) * 1000,
                    "resultado": "llegó a la meta"}
 
        for v in vecinos(esc, actual[0], actual[1]):
            if v not in visitados:
                g_nuevo = g + costo(esc, v[0], v[1])
                frontera.append((g_nuevo + manhattan(v, meta), v, ruta + [v], g_nuevo))
 
    return {"ruta": [], "costo": None,
            "expandidos": expandidos,
            "tiempo_ms": (time.perf_counter() - t0) * 1000,
            "resultado": "sin ruta"}

