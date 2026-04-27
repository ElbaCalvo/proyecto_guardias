class Profesor:
    def __init__(self, id_profesor, nombre, departamento):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.departamento = departamento

class Horario:
    def __init__(self, id_horario, id_profesor, dia_semana, hora, tipo, aula):
        self.id_horario = id_horario
        self.id_profesor = id_profesor
        self.dia_semana = dia_semana
        self.hora = hora
        self.tipo = tipo
        self.aula = aula

class Ausencia:
    def __init__(self, id_ausencia, id_profesor, fecha, hora):
        self.id_ausencia = id_ausencia
        self.id_profesor = id_profesor
        self.fecha = fecha
        self.hora = hora

class Presencia:
    def __init__(self, id_presencia, id_profesor, fecha, hora, presente):
        self.id_presencia = id_presencia
        self.id_profesor = id_profesor
        self.fecha = fecha
        self.hora = hora
        self.presente = presente

class Guardia:
    def __init__(self, id_guardia, fecha, hora, id_profesor_ausente, id_profesor_cubre, aula):
        self.id_guardia = id_guardia
        self.fecha = fecha
        self.hora = hora
        self.id_profesor_ausente = id_profesor_ausente
        self.id_profesor_cubre = id_profesor_cubre
        self.aula = aula