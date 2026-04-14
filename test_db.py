from modules.db.db_manager import get_connection

conn = get_connection()
cursor = conn.cursor()

#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Ana", "Matemáticas"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Pedro", "Física"))

#cursor.execute("INSERT INTO presencia (profesor_id, fecha, estado) VALUES (?, ?, ?)", (1, "2026-04-14", "presente"))
#cursor.execute("INSERT INTO presencia (profesor_id, fecha, estado) VALUES (?, ?, ?)", (2, "2026-04-14", "presente"))

conn.commit()

cursor.execute("SELECT * FROM guardias")
print(cursor.fetchall())

conn.close()
