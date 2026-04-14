from modules.db.db_manager import get_connection
from modules.guardias.reglas import profesor_disponible

def procesar_guardia(profesor_id, fecha, hora, aula):
    if not profesor_disponible(profesor_id, fecha):
        return "No se puede asignar guardia (profesor ausente)"

    conn = get_connection()
    cursor = conn.cursor()

    # Evitar duplicados
    cursor.execute("""
        SELECT id FROM guardias
        WHERE profesor_id = ? AND fecha = ? AND hora = ? AND aula = ?
    """, (profesor_id, fecha, hora, aula))

    existe = cursor.fetchone()

    if existe:
        conn.close()
        return "Ya existe una guardia en ese horario"

    cursor.execute("""
        INSERT INTO guardias (profesor_id, fecha, hora, aula)
        VALUES (?, ?, ?, ?)
    """, (profesor_id, fecha, hora, aula))

    conn.commit()
    conn.close()

    return "Guardia registrada correctamente"