from src.escenario import cargar_escenario, ErrorEscenario, SinSolucion

archivos = ["config/escenario_01.json",
            "config/escenario_02.json",
            "config/escenario_03.json",
            "config/escenario_sin_solucion.json"]

for archivo in archivos:
    print(archivo)
    try:
        esc = cargar_escenario(archivo)
        print("  cargó bien")
        print("  entregas:", esc["entregas"])
        print("  obstáculos:", len(esc["obstaculos"]))
        print("  semilla:", esc["semilla"])
    except SinSolucion as e:
        print("  sin solución:", e)
    except ErrorEscenario as e:
        print("  error en el archivo:", e)