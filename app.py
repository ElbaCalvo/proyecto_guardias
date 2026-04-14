from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from modules.db.db_manager import get_connection
from modules.guardias.motor import procesar_guardia

app = Flask(__name__)

# Datos SIMULADOS de las aulas que requieren cobertura.
necesidades = {
    "08:00": ["Aula 101", "Aula 102"],
    "09:10": ["Aula 201"],
    "11:20": ["Aula 102"],
    "13:00": ["Aula 102", "Aula 201"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():

    conn = get_connection()
    cursor = conn.cursor()

    # Profesores disponibles hoy
    cursor.execute("""
        SELECT p.id, p.nombre
        FROM profesores p
        JOIN presencia pr ON pr.profesor_id = p.id
        WHERE pr.fecha = date('now')
        AND pr.estado = 'presente'
    """)

    profesores_disponibles = cursor.fetchall()

    # Guardias ya asignadas
    cursor.execute("""
        SELECT profesor_id, hora, aula
        FROM guardias
    """)

    guardias_bd = cursor.fetchall()
    conn.close()

    # Convertir a diccionario
    asignadas = {}
    for profesor_id, hora, aula in guardias_bd:
        asignadas[(hora, aula)] = profesor_id

    # Generar tabla desde necesidades
    filas_guardia = []

    for hora, aulas in necesidades.items():
        for aula in aulas:
            filas_guardia.append((hora, aula))

    return render_template(
        "guardias.html",
        filas=filas_guardia,
        profesores=profesores_disponibles,
        asignadas=asignadas
    )

@app.route("/eliminar", methods=["POST"])
def eliminar_guardia():

    hora = request.form["hora"]
    aula = request.form["aula"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM guardias
        WHERE hora = ? AND aula = ?
    """, (hora, aula))

    conn.commit()
    conn.close()

    return redirect(url_for("vista_guardias"))

@app.route("/registrar", methods=["POST"])
def registrar_guardia():

    profesor_id = int(request.form["profesor_id"])
    hora = request.form["hora"]
    aula = request.form["aula"]
    fecha = date.today().isoformat()

    resultado = procesar_guardia(profesor_id, fecha, hora, aula)

    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.id,
            p.nombre,
            COALESCE(pr.estado, 'ausente') as estado
        FROM profesores p
        LEFT JOIN presencia pr 
        ON p.id = pr.profesor_id AND pr.fecha = date('now')
    """)

    profesores = cursor.fetchall()
    conn.close()

    return render_template("presencia.html", profesores=profesores)

@app.route("/toggle_presencia", methods=["POST"])
def toggle_presencia():
    profesor_id = request.form["profesor_id"]
    fecha = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM presencia
        WHERE profesor_id = ? AND fecha = ?
    """, (profesor_id, fecha))

    existe = cursor.fetchone()

    if existe:
        cursor.execute("""
            DELETE FROM presencia
            WHERE profesor_id = ? AND fecha = ?
        """, (profesor_id, fecha))
    else:
        cursor.execute("""
            INSERT INTO presencia (profesor_id, fecha, estado)
            VALUES (?, ?, 'presente')
        """, (profesor_id, fecha))

    conn.commit()
    conn.close()

    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)