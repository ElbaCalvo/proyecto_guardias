import sqlite3
from .models import Profesor, Ausencia

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


def obtener_profesores():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profesores")

        filas = cursor.fetchall()

        # 🔥 Convertir a objetos
        profesores = [
            Profesor(id=f[0], nombre=f[1], departamento=f[2])
            for f in filas
        ]

        return profesores


# -------- AUSENCIAS --------

def registrar_ausencia(profesor_id, fecha, motivo):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ausencias (profesor_id, fecha, motivo) VALUES (?, ?, ?)",
            (profesor_id, fecha, motivo)
        )


def obtener_ausencias():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ausencias")

        filas = cursor.fetchall()

        return [
            Ausencia(id=f[0], profesor_id=f[1], fecha=f[2], motivo=f[3])
            for f in filas
        ]