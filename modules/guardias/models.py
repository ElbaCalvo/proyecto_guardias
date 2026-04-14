class Guardia:
    def __init__(self, id, profesor_id, fecha, hora, nombre_profesor=None):
        self.id = id
        self.profesor_id = profesor_id
        self.fecha = fecha
        self.hora = hora
        self.nombre_profesor = nombre_profesor