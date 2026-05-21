import sqlite3
from .models import Profesor, Ausencia, Presencia, Guardia

DB_PATH = "ies.db"

def get_connection():
    """Establece la conexión con la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# -------- PROFESORES --------

def crear_profesor(nombre, departamento):
    """Inserta un nuevo registro de docente en la tabla profesores."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profesores (nombre, departamento) VALUES (?, ?)",
            (nombre, departamento)
        )
        conn.commit()

def obtener_profesores():
    """Recupera todos los profesores y los mapea a objetos lógicos de la clase Profesor."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_profesor, nombre, departamento FROM profesores")
        filas = cursor.fetchall()

        return [
            Profesor(id_profesor=f[0], nombre=f[1], departamento=f[2])
            for f in filas
        ]

def obtener_profesores_disponibles_en_hora(dia_semana, hora):
    """Devuelve profesores que:
       1. Están presentes hoy.
       2. Tienen esa hora libre en su horario.
       3. Ordenados por quién lleva MENOS guardias totales (Prioridad).
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_profesor, p.nombre, COUNT(g.id_guardia) as total_guardias
            FROM profesores p
            JOIN presencia pr ON p.id_profesor = pr.id_profesor
            JOIN horario h ON p.id_profesor = h.id_profesor
            LEFT JOIN guardias g ON p.id_profesor = g.id_profesor_cubre
            WHERE pr.fecha = date('now') 
              AND pr.presente = 1
              AND h.dia_semana = ? 
              AND h.hora = ? 
              AND h.tipo = 'libre'
            GROUP BY p.id_profesor
            ORDER BY total_guardias ASC, p.nombre ASC
        """, (dia_semana, hora))
        return cursor.fetchall()

def detectar_ausencias_automaticas(dia_semana, hora_lectiva):
    """
    Inserta en la tabla ausencias a los profesores que tienen clase 
    pero no han registrado su presencia hoy.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ausencias (id_profesor, fecha, hora)
            SELECT h.id_profesor, date('now'), h.hora
            FROM horario h
            WHERE h.dia_semana = ? 
              AND h.hora = ? 
              AND h.tipo = 'clase'
              AND h.id_profesor NOT IN (
                  SELECT id_profesor FROM presencia WHERE fecha = date('now')
              )
              AND NOT EXISTS (
                  SELECT 1 FROM ausencias a 
                  WHERE a.id_profesor = h.id_profesor 
                    AND a.fecha = date('now') 
                    AND a.hora = h.hora
              )
        """, (dia_semana, hora_lectiva))
        conn.commit()

# -------- AUSENCIAS --------

def registrar_ausencia(id_profesor, fecha, hora):
    """Inserta manualmente un registro de ausencia para un profesor en una fecha y hora."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ausencias (id_profesor, fecha, hora) VALUES (?, ?, ?)",
            (id_profesor, fecha, hora)
        )
        conn.commit()

def obtener_ausencias():
    """Recupera todas las ausencias almacenadas y las mapea a objetos lógicos Ausencia."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_ausencia, id_profesor, fecha, hora FROM ausencias")
        filas = cursor.fetchall()

        return [
            Ausencia(id_ausencia=f[0], id_profesor=f[1], fecha=f[2], hora=f[3])
            for f in filas
        ]

def obtener_ausencias_con_datos_profesor(dia_semana):
    """Obtiene las ausencias activas del día de hoy cruzando datos con el horario de clase."""
    with get_connection() as conn:
     cursor = conn.cursor()
    cursor.execute("""
        SELECT a.hora, h.aula, p.id_profesor, p.nombre
        FROM ausencias a
        JOIN profesores p ON a.id_profesor = p.id_profesor
        JOIN horario h ON a.id_profesor = h.id_profesor 
                       AND a.hora = h.hora 
                       AND h.dia_semana = ?
        WHERE a.fecha = date('now')
          AND h.tipo = 'clase'
    """, (dia_semana,))
    return cursor.fetchall()

# -------- PRESENCIA --------

def registrar_presencia(id_profesor, fecha, hora, presente):
    """Registra de forma directa un estado de fichaje de presencia en la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO presencia (id_profesor, fecha, hora, presente) VALUES (?, ?, ?, ?)",
            (id_profesor, fecha, hora, presente)
        )
        conn.commit()

def limpiar_tablas_diarias():
    """Mantiene la consistencia del sistema borrando los datos de presencia y ausencia de días anteriores."""
    with get_connection() as conn:
        conn.execute("DELETE FROM presencia WHERE fecha != date('now')")
        conn.execute("DELETE FROM ausencias WHERE fecha != date('now')")
        conn.commit()

def obtener_estado_presencia_todos():
    """Devuelve la lista global de profesores junto a su estado de fichaje del día actual."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_profesor, p.nombre, 
            (SELECT presente FROM presencia 
             WHERE id_profesor = p.id_profesor AND fecha = date('now'))
            FROM profesores p
        """)
        return cursor.fetchall()

def gestionar_fichaje_toggle(profesor_id, dia_semana):
    """Intercambia el estado de asistencia diaria del profesor simulando la acción del hardware."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM presencia WHERE id_profesor = ? AND fecha = date('now')", (profesor_id,))
        existe = cursor.fetchone()

        if existe:
            conn.execute("DELETE FROM presencia WHERE id_profesor = ? AND fecha = date('now')", (profesor_id,))
            conn.execute("""
                INSERT INTO ausencias (id_profesor, fecha, hora)
                SELECT id_profesor, date('now'), hora FROM horario 
                WHERE id_profesor = ? AND dia_semana = ? AND tipo = 'clase'
            """, (profesor_id, dia_semana))
        else:
            conn.execute("DELETE FROM ausencias WHERE id_profesor = ? AND fecha = date('now')", (profesor_id,))
            conn.execute("INSERT INTO presencia (id_profesor, fecha, hora, presente) VALUES (?, date('now'), 0, 1)", (profesor_id,))
        conn.commit()

# -------- GUARDIAS --------

def obtener_guardias():
    """Recupera la lista completa con los registros crudos de todas las guardias."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_guardia, fecha, hora, id_profesor_ausente, id_profesor_cubre, aula FROM guardias")
        filas = cursor.fetchall()
        
        return filas

def obtener_guardias_con_nombre_cubre():
    """Recupera las guardias de hoy enlazando con la tabla profesores para extraer el nombre del sustituto."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.hora, g.aula, p.nombre 
            FROM guardias g
            JOIN profesores p ON g.id_profesor_cubre = p.id_profesor
            WHERE g.fecha = date('now')
        """)
        return cursor.fetchall()

def eliminar_guardia_por_hora_aula(hora, aula):
    """Elimina la asignación de una guardia activa basándose en su tramo horario y su aula."""
    with get_connection() as conn:
        conn.execute("DELETE FROM guardias WHERE hora = ? AND aula = ? AND fecha = date('now')", (hora, aula))
        conn.commit()

def comprobar_guardia_existente(fecha, hora, aula):
    """Comprueba si un aula concreta ya cuenta con una guardia asignada en el mismo tramo horario."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_guardia FROM guardias
            WHERE fecha = ? AND hora = ? AND aula = ?
        """, (fecha, hora, aula))
        return cursor.fetchone() is not None

def registrar_guardia(fecha, hora, id_ausente, id_cubre, aula):
    """Inserta la asignación de la guardia e incrementa el contador histórico del profesor que cubre."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO guardias (fecha, hora, id_profesor_ausente, id_profesor_cubre, aula)
                VALUES (?, ?, ?, ?, ?)
            """, (fecha, hora, id_ausente, id_cubre, aula))
            
            cursor.execute("""
                UPDATE profesores 
                SET guardias_acumuladas = guardias_acumuladas + 1 
                WHERE id_profesor = ?
            """, (id_cubre,))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error en BD: {e}")
        return False
    
def obtener_datos_para_ranking(dia_semana, hora):
    """Extrae las estadísticas de los profesores disponibles para que el motor calcule las prioridades."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_profesor, p.nombre,
                (SELECT COUNT(*) FROM guardias WHERE id_profesor_cubre = p.id_profesor) as total,
                (SELECT COUNT(*) FROM guardias WHERE id_profesor_cubre = p.id_profesor AND fecha >= date('now', 'weekday 1', '-7 days')) as semana,
                (SELECT COUNT(*) FROM horario WHERE id_profesor = p.id_profesor AND tipo = 'clase') as carga
            FROM profesores p
            JOIN presencia pr ON p.id_profesor = pr.id_profesor
            JOIN horario h ON p.id_profesor = h.id_profesor
            WHERE pr.fecha = date('now') AND pr.presente = 1
              AND h.dia_semana = ? AND h.hora = ? AND h.tipo = 'libre'
        """, (dia_semana, hora))
        return cursor.fetchall()
