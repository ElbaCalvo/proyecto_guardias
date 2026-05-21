import modules.db.db_manager as db
from .models import ProfesorDisponible
from .reglas import aplicar_prioridad, profesor_disponible

def obtener_ranking_sustitutos(dia_semana, hora):
    """Genera el ranking ordenado de profesores sustitutos para una hora concreta."""
    datos_brutos = db.obtener_datos_para_ranking(dia_semana, hora) 
    candidatos = [ProfesorDisponible(*d) for d in datos_brutos]
    return aplicar_prioridad(candidatos)

def procesar_guardia(id_ausente, id_cubre, fecha, hora, aula):
    """Valida los criterios de seguridad e introduce la guardia en la base de datos."""
    if id_ausente == id_cubre:
        return "Error: El profesor ausente y el que cubre no pueden ser la misma persona."

    if db.comprobar_guardia_existente(fecha, hora, aula):
        return "Ya existe una guardia registrada para este horario y aula."

    exito = db.registrar_guardia_db(fecha, hora, id_ausente, id_cubre, aula)
    
    if exito:
        return "Guardia registrada correctamente."
    else:
        return "Error al registrar la guardia en la base de datos."