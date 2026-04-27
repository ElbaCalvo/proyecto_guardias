from modules.db.db_manager import get_connection

conn = get_connection()
cursor = conn.cursor()

#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Ana", "Matemáticas"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Pedro", "Física"))

#cursor.execute("INSERT INTO presencia (id_profesor, fecha, presente, hora) VALUES (?, ?, ?, ?)", (1, "2026-04-14", 1, "08:00"))
#cursor.execute("INSERT INTO presencia (id_profesor, fecha, presente, hora) VALUES (?, ?, ?, ?)", (2, "2026-04-14", 0, "09:00"))

conn.commit()

cursor.execute("SELECT * FROM profesores")
print(cursor.fetchall())

cursor.execute("SELECT * FROM horario")
print(cursor.fetchall())

cursor.execute("SELECT * FROM presencia")
print(cursor.fetchall())

cursor.execute("SELECT * FROM ausencias")
print(cursor.fetchall())
conn.close()
