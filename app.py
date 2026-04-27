from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from modules.db.db_manager import get_connection
from modules.guardias.motor import procesar_guardia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_horario, hora, aula, id_profesor FROM horario")
    filas = cursor.fetchall()

    cursor.execute("SELECT id_profesor, nombre FROM profesores")
    profesores = cursor.fetchall()

    cursor.execute("SELECT id_profesor_ausente, id_profesor_cubre, hora, aula FROM guardias WHERE fecha = date('now')")
    guardias_db = cursor.fetchall()
    asignadas = {(g[2], g[3]): {'ausente': g[0], 'cubre': g[1]} for g in guardias_db}

    cursor.execute("""
        SELECT a.hora, h.aula, p.id_profesor, p.nombre
        FROM ausencias a
        JOIN profesores p ON a.id_profesor = p.id_profesor
        JOIN horario h ON a.id_profesor = h.id_profesor AND a.hora = h.hora
        WHERE a.fecha = date('now')
    """)
    ausencias_db = cursor.fetchall()
    
    mapa_ausentes = {}
    for a in ausencias_db:
        mapa_ausentes[(a[0], a[1])] = {'id': a[2], 'nombre': a[3]}

    conn.close()

    return render_template(
        "guardias.html",
        filas=filas,
        mapa_ausentes=mapa_ausentes,
        asignadas=asignadas,
        profesores=profesores,
        fecha_actual=date.today().isoformat()
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
    id_ausente = int(request.form["id_profesor_ausente"])
    id_cubre = int(request.form["id_profesor_cubre"])
    hora = request.form["hora"]
    aula = request.form["aula"]
    fecha = request.form["fecha"]

    # Llamamos a tu motor con los nuevos parámetros
    resultado = procesar_guardia(id_ausente, id_cubre, fecha, hora, aula)
    
    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    conn = get_connection()
    cursor = conn.cursor()

    # Ajustado a id_profesor
    cursor.execute("""
        SELECT 
            p.id_profesor,
            p.nombre,
            COALESCE(pr.presente, 0) as presente
        FROM profesores p
        LEFT JOIN presencia pr 
        ON p.id_profesor = pr.id_profesor AND pr.fecha = date('now')
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
        SELECT id_presencia FROM presencia
        WHERE id_profesor = ? AND fecha = ?
    """, (profesor_id, fecha))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("DELETE FROM presencia WHERE id_profesor = ? AND fecha = ?", (profesor_id, fecha))
    else:
        cursor.execute("""
            INSERT INTO presencia (id_profesor, fecha, hora, presente) 
            VALUES (?, ?, 0, 1)
        """, (profesor_id, fecha))

    conn.commit()
    conn.close()

    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)