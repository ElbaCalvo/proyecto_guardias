from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
import modules.db.db_manager as db
from modules.guardias.motor import procesar_guardia

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():
    dia_actual = datetime.now().isoweekday()
    fecha_hoy = date.today().isoformat()
    
    filas = db.obtener_ausencias_con_datos_profesor(dia_actual)
    
    guardias_db = db.obtener_guardias_con_nombre_cubre()
    asignadas = {(g[0], g[1]): {'cubre': g[2]} for g in guardias_db}

    sustitutos_por_hora = {}
    for f in filas:
        hora_ausencia = f[0]
        if hora_ausencia not in sustitutos_por_hora:
            sustitutos_por_hora[hora_ausencia] = db.obtener_profesores_disponibles_en_hora(dia_actual, hora_ausencia)

    return render_template(
        "guardias.html", 
        filas=filas,
        sustitutos_por_hora=sustitutos_por_hora, # Pasamos el diccionario
        asignadas=asignadas,
        fecha_actual=fecha_hoy
    )

@app.route("/registrar", methods=["POST"])
def registrar_guardia():
    procesar_guardia(
        int(request.form["id_profesor_ausente"]),
        int(request.form["id_profesor_cubre"]),
        request.form["fecha"],
        request.form["hora"],
        request.form["aula"]
    )
    return redirect(url_for("vista_guardias"))

@app.route("/eliminar", methods=["POST"])
def eliminar_guardia():
    db.eliminar_guardia_por_hora_aula(request.form["hora"], request.form["aula"])
    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    db.limpiar_tablas_diarias()
    profesores = db.obtener_estado_presencia_todos()
    return render_template("presencia.html", profesores=profesores)

@app.route("/toggle_presencia", methods=["POST"])
def toggle_presencia():
    pid = request.form["profesor_id"]
    dia = datetime.now().isoweekday() 
    db.gestionar_fichaje_toggle(pid, dia)
    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)