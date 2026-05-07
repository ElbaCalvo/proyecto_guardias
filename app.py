from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
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
    dia_actual = datetime.now().isoweekday()

    cursor.execute("""
        SELECT a.hora, h.aula, p.id_profesor, p.nombre
        FROM ausencias a
        JOIN profesores p ON a.id_profesor = p.id_profesor
        JOIN horario h ON a.id_profesor = h.id_profesor AND a.hora = h.hora AND h.dia_semana = ?
        WHERE a.fecha = date('now')
    """, (dia_actual,))
    filas = cursor.fetchall()
    
    mapa_ausentes = {}
    for f in filas:
        h, au, id_p, nom_p = f
        mapa_ausentes[(h, au)] = {'id': id_p, 'nombre': nom_p}

    cursor.execute("""
        SELECT p.id_profesor, p.nombre FROM profesores p
        JOIN presencia pr ON p.id_profesor = pr.id_profesor
        WHERE pr.fecha = date('now') AND pr.presente = 1
    """)
    profesores_lista = cursor.fetchall()

    cursor.execute("""
        SELECT g.hora, g.aula, p.nombre 
        FROM guardias g
        JOIN profesores p ON g.id_profesor_cubre = p.id_profesor
        WHERE g.fecha = date('now')
    """)
    guardias_db = cursor.fetchall()
    
    asignadas = {(g[0], g[1]): {'cubre': g[2]} for g in guardias_db}

    conn.close()
    return render_template(
        "guardias.html", 
        filas=filas,
        mapa_ausentes=mapa_ausentes, 
        profesores=profesores_lista,
        asignadas=asignadas, # <-- Ahora el HTML recibirá las guardias hechas
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

    resultado = procesar_guardia(id_ausente, id_cubre, fecha, hora, aula)
    
    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM presencia WHERE fecha != date('now')")
    cursor.execute("DELETE FROM ausencias WHERE fecha != date('now')")
    conn.commit()

    cursor.execute("""
        SELECT 
            p.id_profesor, 
            p.nombre, 
            (SELECT presente FROM presencia 
             WHERE id_profesor = p.id_profesor 
             AND fecha = date('now')) as esta_presente
        FROM profesores p
    """)
    profesores = cursor.fetchall()
    conn.close()
    return render_template("presencia.html", profesores=profesores)

@app.route("/toggle_presencia", methods=["POST"])
def toggle_presencia():
    profesor_id = request.form["profesor_id"]
    dia_semana_hoy = datetime.now().isoweekday() 

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM presencia 
        WHERE id_profesor = ? AND fecha = date('now')
    """, (profesor_id,))
    esta_presente = cursor.fetchone()

    if esta_presente:
        cursor.execute("DELETE FROM presencia WHERE id_profesor = ? AND fecha = date('now')", (profesor_id,))
        
        cursor.execute("""
            INSERT INTO ausencias (id_profesor, fecha, hora)
            SELECT id_profesor, date('now'), hora 
            FROM horario 
            WHERE id_profesor = ? AND dia_semana = ? AND tipo = 'clase'
        """, (profesor_id, dia_semana_hoy))
        
    else:
        cursor.execute("DELETE FROM ausencias WHERE id_profesor = ? AND fecha = date('now')", (profesor_id,))
        
        cursor.execute("""
            INSERT INTO presencia (id_profesor, fecha, hora, presente) 
            VALUES (?, date('now'), 0, 1)
        """, (profesor_id,))

    conn.commit()
    conn.close()
    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)