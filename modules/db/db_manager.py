import sqlite3
from .models import Profesor, Ausencia, Presencia, Guardia

DB_PATH = "ies.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# -------- PROFESORES --------

def crear_profesor(nombre, departamento):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profesores (nombre, departamento) VALUES (?, ?)",
            (nombre, departamento)
        )
        conn.commit()

def obtener_profesores():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_profesor, nombre, departamento FROM profesores")
        filas = cursor.fetchall()

        return [
            Profesor(id_profesor=f[0], nombre=f[1], departamento=f[2])
            for f in filas
        ]

def obtener_profesores_disponibles_hoy():
    """Para el desplegable: solo los que han fichado 'presente' hoy"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id_profesor, p.nombre FROM profesores p
            JOIN presencia pr ON p.id_profesor = pr.id_profesor
            WHERE pr.fecha = date('now') AND pr.presente = 1
        """)
        return cursor.fetchall()

# -------- AUSENCIAS --------

def registrar_ausencia(id_profesor, fecha, hora):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ausencias (id_profesor, fecha, hora) VALUES (?, ?, ?)",
            (id_profesor, fecha, hora)
        )
        conn.commit()

def obtener_ausencias():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_ausencia, id_profesor, fecha, hora FROM ausencias")
        filas = cursor.fetchall()

        return [
            Ausencia(id_ausencia=f[0], id_profesor=f[1], fecha=f[2], hora=f[3])
            for f in filas
        ]

def obtener_ausencias_con_datos_profesor(dia_semana):
    """Esta es la que necesita la tabla de guardias para mostrar el NOMBRE y el AULA"""
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
        """, (dia_semana,))
        return cursor.fetchall()

# -------- PRESENCIA --------

def registrar_presencia(id_profesor, fecha, hora, presente):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO presencia (id_profesor, fecha, hora, presente) VALUES (?, ?, ?, ?)",
            (id_profesor, fecha, hora, presente)
        )
        conn.commit()

def limpiar_tablas_diarias():
    """Borra presencia y ausencias que no sean de hoy al cargar presencia"""
    with get_connection() as conn:
        conn.execute("DELETE FROM presencia WHERE fecha != date('now')")
        conn.execute("DELETE FROM ausencias WHERE fecha != date('now')")
        conn.commit()

def obtener_estado_presencia_todos():
    """Devuelve la lista de profesores con un 1 o 0 si están presentes hoy"""
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
    """Toda la lógica de 'si está presente lo borro y creo ausencia' metida aquí"""
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

def registrar_guardia(fecha, hora, id_profesor_ausente, id_profesor_cubre, aula):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO guardias (fecha, hora, id_profesor_ausente, id_profesor_cubre, aula) 
               VALUES (?, ?, ?, ?, ?)""",
            (fecha, hora, id_profesor_ausente, id_profesor_cubre, aula)
        )
        conn.commit()

def obtener_guardias():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_guardia, fecha, hora, id_profesor_ausente, id_profesor_cubre, aula FROM guardias")
        filas = cursor.fetchall()
        
        return filas

def obtener_guardias_con_nombre_cubre():
    """Necesaria para que en la tabla de guardias salga el NOMBRE del que cubre"""
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
    """Para la ruta @app.route('/eliminar')"""
    with get_connection() as conn:
        conn.execute("DELETE FROM guardias WHERE hora = ? AND aula = ? AND fecha = date('now')", (hora, aula))
        conn.commit()
