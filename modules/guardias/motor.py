from modules.db.db_manager import get_connection

def procesar_guardia(id_profesor_ausente, id_profesor_cubre, fecha, hora, aula):
    """
    Registra una guardia sustituyendo a un profesor ausente.
    """
    
    if id_profesor_ausente == id_profesor_cubre:
        return "Error: El profesor ausente y el que cubre no pueden ser la misma persona."

    conn = get_connection()
    cursor = conn.cursor()

    # Evitar duplicados
    cursor.execute("""
        SELECT id_guardia FROM guardias
        WHERE fecha = ? AND hora = ? AND aula = ?
    """, (fecha, hora, aula))

    existe = cursor.fetchone()

    if existe:
        conn.close()
        return "Ya existe una guardia registrada para este horario y aula."

    # Insertar el registro
    try:
        cursor.execute("""
            INSERT INTO guardias (fecha, hora, id_profesor_ausente, id_profesor_cubre, aula)
            VALUES (?, ?, ?, ?, ?)
        """, (fecha, hora, id_profesor_ausente, id_profesor_cubre, aula))

        conn.commit()
        resultado = "Guardia registrada correctamente."
    except Exception as e:
        conn.rollback()
        resultado = f"Error al registrar la guardia: {str(e)}"
    finally:
        conn.close()

    return resultado