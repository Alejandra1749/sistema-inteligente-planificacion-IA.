# minimax y alfa-beta 
from src.busqueda_local import calcular_matriz


def calcular_valores(esc, matriz):
    ganancia = 30 #supuesto del modelo
    directo = matriz[(esc["inicio"], esc["destino"])]
    valores = {}
    for e in esc["entregas"]:
        desvio = matriz[(esc["inicio"], e)] + matriz[(e, esc["destino"])] - directo
        valores[e] = ganancia - desvio
    return valores


# Un estado es una tupla
# turno 0 = MAX, turno 1 = MIN 

def estado_inicial(esc):
    return (tuple(esc["entregas"]), 0, 0, 0)


def acciones(estado):
    return list(estado[0])


def es_terminal(estado):
    return len(estado[0]) == 0


def aplicar(estado, entrega, valores):
    libres, pts_max, pts_min, turno = estado
    nuevas = tuple(e for e in libres if e != entrega)
    if turno == 0:
        return (nuevas, pts_max + valores[entrega], pts_min, 1)
    return (nuevas, pts_max, pts_min + valores[entrega], 0)


def utilidad(estado):
    # lo que lleva MAX menos lo que lleva MIN
    return estado[1] - estado[2]

##minimax####
def evaluacion(estado, valores):
    # evaluación aproximada
    libres, pts_max, pts_min, turno = estado
    restantes = sorted([valores[e] for e in libres], reverse=True)
    for v in restantes:
        if turno == 0:
            pts_max += v
        else:
            pts_min += v
        turno = 1 - turno
    return pts_max - pts_min


def minimax(estado, valores, profundidad, contador):
    contador[0] += 1# cuento cada nodo que visito

    if es_terminal(estado):
        return utilidad(estado)
    if profundidad == 0:# llega al límite
        return evaluacion(estado, valores)

    if estado[3] == 0: # turno de MAX
        mejor = -1000
        for a in acciones(estado):
            v = minimax(aplicar(estado, a, valores), valores, profundidad - 1, contador)
            if v > mejor:
                mejor = v
        return mejor
    else:   # turno de MIN
        mejor = 1000
        for a in acciones(estado):
            v = minimax(aplicar(estado, a, valores), valores, profundidad - 1, contador)
            if v < mejor:
                mejor = v
        return mejor


def mejor_jugada(estado, valores, profundidad):
    mejor = None
    mejor_valor = -1000
    for a in acciones(estado):
        v = minimax(aplicar(estado, a, valores), valores, profundidad - 1, [0])
        if v > mejor_valor:
            mejor_valor = v
            mejor = a
    return mejor, mejor_valor


##alfa-beta
def alfabeta(estado, valores, profundidad, alfa, beta, contador, ordenar=False):
    # contador = [nodos visitados, podas hechas]
    contador[0] += 1

    if es_terminal(estado):
        return utilidad(estado)
    if profundidad == 0:
        return evaluacion(estado, valores)

    lista = acciones(estado)
    if ordenar:                        
        lista = sorted(lista, key=valores.get, reverse=True)

    if estado[3] == 0:# turno de MAX
        mejor = -1000
        for a in lista:
            v = alfabeta(aplicar(estado, a, valores), valores, profundidad - 1,
                         alfa, beta, contador, ordenar)
            if v > mejor:
                mejor = v
            if mejor > alfa:
                alfa = mejor
            if alfa >= beta: # poda
                contador[1] += 1
                break
        return mejor
    else: # turno de MIN
        mejor = 1000
        for a in lista:
            v = alfabeta(aplicar(estado, a, valores), valores, profundidad - 1,
                         alfa, beta, contador, ordenar)
            if v < mejor:
                mejor = v
            if mejor < beta:
                beta = mejor
            if alfa >= beta:  # poda
                contador[1] += 1
                break
        return mejor