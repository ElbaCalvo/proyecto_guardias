from .reglas import puede_entrar

def procesar_entrada(guardia):
    if puede_entrar(guardia):
        return f"Entrada registrada para {guardia.nombre}"
    else:
        return f"Entrada denegada para {guardia.nombre}"