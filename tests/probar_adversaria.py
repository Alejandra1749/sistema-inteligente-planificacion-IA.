from src.escenario import cargar_escenario
from src.busqueda_local import calcular_matriz
from src.adversaria import calcular_valores, estado_inicial, acciones, aplicar, es_terminal, utilidad
import time
from src.adversaria import minimax
from src.adversaria import alfabeta

esc = cargar_escenario("config/escenario_04.json")
matriz = calcular_matriz(esc)
valores = calcular_valores(esc, matriz)

print("Valor de cada entrega:")
for e in valores:
    print("  ", e, "->", valores[e])

estado = estado_inicial(esc)
print()
print("Estado inicial:", estado)
print("Acciones legales:", len(acciones(estado)))

# juego de prueba
while not es_terminal(estado):
    estado = aplicar(estado, acciones(estado)[0], valores)
print("Estado final:", estado)
print("Utilidad:", utilidad(estado))


print()
for prof in [8, 4, 2]:
    contador = [0]
    t0 = time.perf_counter()
    valor = minimax(estado_inicial(esc), valores, prof, contador)
    ms = (time.perf_counter() - t0) * 1000
    print("profundidad", prof, "-> valor", valor, " nodos visitados", contador[0],
          " tiempo", round(ms, 1), "ms")


print()
print("Minimax contra alfa-beta")
for prof in [8, 4]:
    cm = [0]
    vm = minimax(estado_inicial(esc), valores, prof, cm)

    for ordenar in [False, True]:
        ca = [0, 0]
        t0 = time.perf_counter()
        va = alfabeta(estado_inicial(esc), valores, prof, -1000, 1000, ca, ordenar)
        ms = (time.perf_counter() - t0) * 1000
        print("profundidad", prof, " ordenar", ordenar)
        print("   valor minimax", vm, " valor alfa-beta", va, " iguales:", vm == va)
        print("   nodos minimax", cm[0], " nodos alfa-beta", ca[0],
              " podados", cm[0] - ca[0], " podas", ca[1])
        print("   tiempo", round(ms, 1), "ms")