from src.escenario import cargar_escenario
from src.teoria_juegos import construir_matriz
from src.teoria_juegos import mejores_respuestas, domina, equilibrios_nash

esc = cargar_escenario("config/escenario_04.json")
matriz = construir_matriz(esc)

print("Matriz de pagos (jugador 1, jugador 2)")
for jugada in matriz:
    print(jugada, "->", matriz[jugada])

print()
print("Mejores respuestas")
for otro in [1, 2, 3]:
    print("Si el otro reserva", otro)
    print("   jugador 1 reserva", mejores_respuestas(matriz, 0, otro))
    print("   jugador 2 reserva", mejores_respuestas(matriz, 1, otro))

print()
print("Dominancia")
for jugador in [0, 1]:
    for a in [1, 2, 3]:
        for b in [1, 2, 3]:
            tipo = domina(matriz, jugador, a, b)
            if a != b and tipo != "no":
                print("Jugador", jugador + 1, "- reservar", a, "domina a reservar", b, "(" + tipo + ")")

print()
print("Equilibrios de Nash:", equilibrios_nash(matriz))