from modules.db.db_manager import get_connection

def profesor_disponible(id_profesor, fecha):
    """Comprueba que el profesor no esté en la lista de ausencias"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ausencias WHERE id_profesor = ? AND fecha = ?", (id_profesor, fecha))
        return cursor.fetchone() is None

def aplicar_prioridad(lista_candidatos):
    """Ordena según los 3 criterios del PDF"""
    return sorted(lista_candidatos, key=lambda p: (
        p.total_guardias, 
        p.guardias_semana, 
        p.carga_lectiva
    ))