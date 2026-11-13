#revisar el escenario
import json

# Tipos de errores
class ErrorEscenario(Exception):
    pass          # Si esta mal escrito o con datos invalidos

class SinSolucion(Exception):
    pass          # si no se puede llegar a un punto


campos = ["nombre", "tamano", "inicio", "destino", "entregas", "obstaculos",
          "costos", "movimientos", "recursos", "competidor", "semilla"]


def cargar_escenario(ruta):

    # va a abrir el json
    try:
        with open(ruta, encoding="utf-8") as archivo:
            esc = json.load(archivo)
    except FileNotFoundError:
        raise ErrorEscenario("No existe el archivo " + ruta)
    except json.JSONDecodeError:
        raise ErrorEscenario("No es un json valido")

    # verifica que esten todos los campos
    for campo in campos:
        if campo not in esc:
            raise ErrorEscenario("Falta el campo: " + campo)

    # revisar tamaño 12 y costos
    if esc["tamano"] != 12:
        raise ErrorEscenario("El tamaño debe ser 12")

    if len(esc["costos"]) != 12:
        raise ErrorEscenario("La matriz de costos debe tener 12 filas")
    for fila in esc["costos"]:
        if len(fila) != 12:
            raise ErrorEscenario("Cada fila de costos debe tener 12 valores")
        for valor in fila:
            if valor <= 0:
                raise ErrorEscenario("Los costos deben ser mayores que 0")

    #revisa los movimientos y entregas que no sean menor a 3
    if len(esc["entregas"]) < 3:
        raise ErrorEscenario("Debe haber al menos 3 entregas")
    if len(esc["movimientos"]) == 0:
        raise ErrorEscenario("Debe haber al menos un movimiento permitido")

    # Convertir las listas a tuplas 
    esc["inicio"] = tuple(esc["inicio"])
    esc["destino"] = tuple(esc["destino"])
    esc["entregas"] = [tuple(p) for p in esc["entregas"]]
    esc["obstaculos"] = [tuple(p) for p in esc["obstaculos"]]
    esc["movimientos"] = [tuple(m) for m in esc["movimientos"]]

    # revisar que los puntos estén dentro del mapa
    for punto in puntos_clave(esc):
        fila, columna = punto
        if fila < 0 or fila > 11 or columna < 0 or columna > 11:
            raise ErrorEscenario("El punto " + str(punto) + " está fuera del mapa")
        if punto in esc["obstaculos"]:
            raise ErrorEscenario("El punto " + str(punto) + " está sobre un obstáculo")

    # revisar competidor y semilla
    if esc["competidor"]["recurso"] not in esc["recursos"]:
        raise ErrorEscenario("El recurso del competidor no está en 'recursos'")
    if not isinstance(esc["semilla"], int):
        raise ErrorEscenario("La semilla debe ser un número entero")

    # revisar que se pueda llegar a todos los puntos
    alcanzables = _puntos_alcanzables(esc)
    for punto in puntos_clave(esc):
        if punto not in alcanzables:
            raise SinSolucion("No se puede llegar al punto " + str(punto))

    return esc

#funciones de los otros modulos

def puntos_clave(esc):
    #inicio, entregas y destinos
    return [esc["inicio"]] + esc["entregas"] + [esc["destino"]]


def es_transitable(esc, fila, columna):
    dentro = 0 <= fila < 12 and 0 <= columna < 12
    return dentro and (fila, columna) not in esc["obstaculos"]


def costo(esc, fila, columna):
    return esc["costos"][fila][columna]


def vecinos(esc, fila, columna):
    #lista de casillas a las que se puede mover
    lista = []
    for mover_fila, mover_columna in esc["movimientos"]:
        nueva_fila = fila + mover_fila
        nueva_columna = columna + mover_columna
        if es_transitable(esc, nueva_fila, nueva_columna):
            lista.append((nueva_fila, nueva_columna))
    return lista


def _puntos_alcanzables(esc):
    visitadas = [esc["inicio"]]
    pendientes = [esc["inicio"]]
    while len(pendientes) > 0:
        fila, columna = pendientes.pop()
        for vecino in vecinos(esc, fila, columna):
            if vecino not in visitadas:
                visitadas.append(vecino)
                pendientes.append(vecino)
    return visitadas