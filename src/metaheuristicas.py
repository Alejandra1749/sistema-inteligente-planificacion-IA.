# metaheurísticas
import math
import random
import time
from src.busqueda_local import costo_orden


def recocido(esc, matriz, orden_inicial, T=20, enfriamiento=0.95,
             T_final=0.1, repeticiones=10):
    t0 = time.perf_counter()
    actual = orden_inicial[:]
    costo_actual = costo_orden(esc, matriz, actual)
    mejor = actual[:]
    mejor_costo = costo_actual
    evaluaciones = 1

    while T > T_final:
        for _ in range(repeticiones):
            # vecino
            i, j = random.sample(range(len(actual)), 2)
            vecino = actual[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            costo_vecino = costo_orden(esc, matriz, vecino)
            evaluaciones += 1

            delta = costo_vecino - costo_actual     
            if delta <= 0:
                aceptar = True  # si es mejor se acepta
            else:
                p = math.exp(-delta / T) # probabilidad de aceptar uno peor
                aceptar = random.random() < p 

            if aceptar:
                actual = vecino
                costo_actual = costo_vecino
                if costo_actual < mejor_costo:      
                    mejor = actual[:]
                    mejor_costo = costo_actual

        T = T * enfriamiento # enfriamiento

    return {"orden": mejor,
            "costo": mejor_costo,
            "evaluaciones": evaluaciones,
            "tiempo_ms": (time.perf_counter() - t0) * 1000}


def torneo(poblacion, costos):
    #Elije 2 al azar, gana el de menor costo
    i, j = random.sample(range(len(poblacion)), 2)
    if costos[i] < costos[j]:
        return poblacion[i]
    return poblacion[j]


def cruza(padre1, padre2):
    #una parte del padre 1 y el resto del 2
    a, b = sorted(random.sample(range(len(padre1)), 2))
    hijo = padre1[a:b]
    for entrega in padre2:
        if entrega not in hijo:
            hijo.append(entrega)
    return hijo


def genetico(esc, matriz, tam=30, generaciones=35, prob_mutacion=0.1):
    t0 = time.perf_counter()

    # población inicial al azar
    poblacion = []
    for _ in range(tam):
        orden = esc["entregas"][:]
        random.shuffle(orden)
        poblacion.append(orden)

    mejor = None
    mejor_costo = None
    evaluaciones = 0
    historial = [] # mejor costo de cada generación

    for g in range(generaciones):
        # evaluar a todos
        costos = []
        for individuo in poblacion:
            c = costo_orden(esc, matriz, individuo)
            costos.append(c)
            evaluaciones += 1
            if mejor_costo is None or c < mejor_costo:
                mejor = individuo[:]
                mejor_costo = c
        historial.append(mejor_costo)

        # nueva generación
        nueva = [mejor[:]] # el mejor pasa directo
        while len(nueva) < tam:
            padre1 = torneo(poblacion, costos)
            padre2 = torneo(poblacion, costos)
            hijo = cruza(padre1, padre2)
            if random.random() < prob_mutacion:# mutación
                i, j = random.sample(range(len(hijo)), 2)
                hijo[i], hijo[j] = hijo[j], hijo[i]
            nueva.append(hijo)
        poblacion = nueva

    return {"orden": mejor,
            "costo": mejor_costo,
            "evaluaciones": evaluaciones,
            "historial": historial,
            "tiempo_ms": (time.perf_counter() - t0) * 1000}