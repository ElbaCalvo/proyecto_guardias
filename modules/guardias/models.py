class Guardia:
    """Representa una clase que se ha quedado sin profesor"""
    def __init__(self, id_guardia, fecha, hora, id_profesor_ausente, id_profesor_cubre, aula, nombre_ausente=None, nombre_cubre=None):
        self.id_guardia = id_guardia
        self.fecha = fecha
        self.hora = hora
        self.id_profesor_ausente = id_profesor_ausente
        self.id_profesor_cubre = id_profesor_cubre
        self.aula = aula
    
class ProfesorDisponible:
    """Representa a un candidato para cubrir una guardia con sus méritos"""
    def __init__(self, id_profesor, nombre, total_guardias, guardias_semana, carga_lectiva):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.total_guardias = total_guardias
        self.guardias_semana = guardias_semana
        self.carga_lectiva = carga_lectiva