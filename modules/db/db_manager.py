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

# -------- PRESENCIA --------

def registrar_presencia(id_profesor, fecha, hora, presente):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO presencia (id_profesor, fecha, hora, presente) VALUES (?, ?, ?, ?)",
            (id_profesor, fecha, hora, presente)
        )
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