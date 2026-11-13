#teoría de juegos

def pagos(esc, k1, k2):
    # vehículos que reserva cada jugador
    vehiculos = esc["recursos"]["transporte"]
    precio = esc["recursos"]["costo_transporte"]
    ganancia = 20# ganancia por vehículo usado

    total = k1 + k2
    if total > vehiculos:
        precio = precio * esc["competidor"]["factor"]
        usa1 = k1 * vehiculos / total# se reparten en proporción a lo que pidieron
        usa2 = k2 * vehiculos / total
    else:
        usa1 = k1
        usa2 = k2

    pago1 = ganancia * usa1 - precio * k1
    pago2 = ganancia * usa2 - precio * k2
    return (pago1, pago2)


def construir_matriz(esc):
    matriz = {}
    for k1 in [1, 2, 3]:
        for k2 in [1, 2, 3]:
            matriz[(k1, k2)] = pagos(esc, k1, k2)
    return matriz



def pago(matriz, jugador, mia, otro):
    if jugador == 0:
        return matriz[(mia, otro)][0]
    return matriz[(otro, mia)][1]


def mejores_respuestas(matriz, jugador, otro):
    # estrategias que dan el mayor pago si el otro reserva otro
    mejor = pago(matriz, jugador, 1, otro)
    for k in [1, 2, 3]:
        if pago(matriz, jugador, k, otro) > mejor:
            mejor = pago(matriz, jugador, k, otro)

    lista = []
    for k in [1, 2, 3]:
        if pago(matriz, jugador, k, otro) == mejor:
            lista.append(k)
    return lista


def domina(matriz, jugador, a, b):

    mayores = 0
    iguales = 0
    for otro in [1, 2, 3]:
        pa = pago(matriz, jugador, a, otro)
        pb = pago(matriz, jugador, b, otro)
        if pa < pb:
            return "no"                  
        if pa > pb:
            mayores += 1
        else:
            iguales += 1

    if iguales == 0:
        return "estricta" # mejor en todos los casos
    if mayores > 0:
        return "débil"                  
    return "no"


def equilibrios_nash(matriz):
    lista = []
    for k1 in [1, 2, 3]:
        for k2 in [1, 2, 3]:
            
            if k1 in mejores_respuestas(matriz, 0, k2) and k2 in mejores_respuestas(matriz, 1, k1):
                lista.append((k1, k2))
    return lista