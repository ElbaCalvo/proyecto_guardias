import sqlite3
import os

DB_PATH = "ies.db"
BASE_DIR = os.path.dirname(__file__)


def init_db():
    """Crea las tablas iniciales leyendo el archivo schema.sql."""
    schema_path = os.path.join(BASE_DIR, "schema.sql")

    # Conexión a la base de datos y ejecución del script de creación de tablas
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        with open(schema_path, "r") as f:
            conn.executescript(f.read())


if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada")