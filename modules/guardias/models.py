class Guardia:
    def __init__(self, id_guardia, fecha, hora, id_profesor_ausente, id_profesor_cubre, aula, nombre_ausente=None, nombre_cubre=None):
        self.id_guardia = id_guardia
        self.fecha = fecha
        self.hora = hora
        self.id_profesor_ausente = id_profesor_ausente
        self.id_profesor_cubre = id_profesor_cubre
        self.aula = aula