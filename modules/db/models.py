class Profesor:
    def __init__(self, id, nombre, departamento):
        self.id = id
        self.nombre = nombre
        self.departamento = departamento


class Horario:
    def __init__(self, id, profesor_id, dia, hora):
        self.id = id
        self.profesor_id = profesor_id
        self.dia = dia
        self.hora = hora


class Ausencia:
    def __init__(self, id, profesor_id, fecha, motivo):
        self.id = id
        self.profesor_id = profesor_id
        self.fecha = fecha
        self.motivo = motivo


class Presencia:
    def __init__(self, id, profesor_id, fecha, estado):
        self.id = id
        self.profesor_id = profesor_id
        self.fecha = fecha
        self.estado = estado


class Guardia:
    def __init__(self, id, profesor_id, fecha, hora):
        self.id = id
        self.profesor_id = profesor_id
        self.fecha = fecha
        self.hora = hora