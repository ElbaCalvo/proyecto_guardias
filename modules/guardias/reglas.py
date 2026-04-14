from modules.db.db_manager import get_connection


def profesor_disponible(profesor_id, fecha):
    conn = get_connection()
    cursor = conn.cursor()

    # Comprobamos si está en ausencias ese día
    cursor.execute("""
        SELECT id FROM ausencias
        WHERE profesor_id = ? AND fecha = ?
    """, (profesor_id, fecha))

    ausencia = cursor.fetchone()

    conn.close()

    # Si hay ausencia → no disponible
    return ausencia is None