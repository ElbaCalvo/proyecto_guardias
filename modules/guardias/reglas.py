from modules.db.db_manager import get_connection


def profesor_disponible(id_profesor, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    # Comprobamos si está en ausencias ese día
    cursor.execute("""
        SELECT id FROM ausencias
        WHERE profesor_id = ? AND fecha = ?
    """, (id_profesor, fecha))

    ausencia = cursor.fetchone()

    conn.close()

    # Si hay ausencia entonces no disponible
    return ausencia is None