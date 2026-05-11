from modules.db.db_manager import get_connection
import random

conn = get_connection()
cursor = conn.cursor()

#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Ana", "Matemáticas"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Pedro", "Física"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Lucía", "Lengua"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Carlos", "Inglés"))
#cursor.execute("INSERT INTO profesores (nombre, departamento) VALUES (?, ?)", ("Marta", "Dibujo"))

#cursor.execute("INSERT INTO presencia (id_profesor, fecha, presente, hora) VALUES (?, ?, ?, ?)", (1, "2026-04-14", 1, "08:00"))
#cursor.execute("INSERT INTO presencia (id_profesor, fecha, presente, hora) VALUES (?, ?, ?, ?)", (2, "2026-04-14", 0, "09:00"))

# Actualizamos el id_profesor en la tabla horario
# Cambiamos el 1 por el 7 (Ana)
#cursor.execute("UPDATE horario SET id_profesor = 7 WHERE id_profesor = 1")

# Cambiamos el 2 por el 8 (Pedro)
#cursor.execute("UPDATE horario SET id_profesor = 8 WHERE id_profesor = 2")

todos_los_profes = [7, 8, 9, 10, 11]
aulas = ['ESO1', 'ESO2', 'ESO3', 'ESO4', 'BAC1', 'BAC2']

print("Limpiando horarios y transformando todo en Clase o Libre...")

# BORRAMOS para regenerar de forma limpia
cursor.execute(f"DELETE FROM horario WHERE id_profesor IN ({','.join(map(str, todos_los_profes))})")
conn.commit()

for id_p in todos_los_profes:
    for d in range(1, 6):   # Lunes a Viernes
        for h in range(1, 7):  # 1ª a 6ª hora
            # Ahora solo hay dos opciones: clase (70%) o libre (30%)
            tipo = random.choices(['clase', 'libre'], weights=[70, 30])[0]
            
            if tipo == 'clase':
                aula = random.choice(aulas)
            else:
                aula = None # Libre
                
            cursor.execute("""
                INSERT INTO horario (id_profesor, dia_semana, hora, tipo, aula) 
                VALUES (?, ?, ?, ?, ?)
            """, (id_p, dia_semana:=d, hora:=h, tipo, aula))

conn.commit()

cursor.execute("SELECT * FROM profesores")
print(cursor.fetchall())

cursor.execute("SELECT * FROM horario")
print(cursor.fetchall())

cursor.execute("SELECT * FROM presencia")
print(cursor.fetchall())

cursor.execute("SELECT * FROM ausencias")
print(cursor.fetchall())

cursor.execute("SELECT * FROM guardias")
print(cursor.fetchall())
conn.close()
