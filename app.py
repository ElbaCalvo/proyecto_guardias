from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import date, datetime
import modules.db.db_manager as db
from modules.guardias.motor import obtener_ranking_sustitutos, procesar_guardia

app = Flask(__name__)
app.secret_key = 'proyecto_guardias_clave_secreta'

try:
    from mfrc522 import SimpleMFRC522
    lector_rfid = SimpleMFRC522()
except ImportError:
    lector_rfid = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():
    ahora = datetime.now()
    dia_actual = datetime.now().isoweekday()
    hora_reloj = ahora.hour
    min_reloj = ahora.minute
    fecha_hoy = date.today().isoformat()
    
    # 1ª Hora (08:30 - 09:20) -> Se marca ausencia a las 08:45
    if (hora_reloj == 8 and min_reloj >= 45) or (hora_reloj == 9 and min_reloj < 20):
        db.detectar_ausencias_automaticas(dia_actual, 1)
        
    # 2ª Hora (09:20 - 10:10) -> Se marca ausencia a las 09:35
    elif (hora_reloj == 9 and min_reloj >= 35) or (hora_reloj == 10 and min_reloj < 10):
        db.detectar_ausencias_automaticas(dia_actual, 2)
        
    # 3ª Hora (10:10 - 11:00) -> Se marca ausencia a las 10:25
    elif (hora_reloj == 10 and min_reloj >= 25) or (hora_reloj == 11 and min_reloj < 0):
        db.detectar_ausencias_automaticas(dia_actual, 3)
        
    # RECREO (11:00 - 11:30)
    
    # 4ª Hora (11:30 - 12:20) -> Se marca ausencia a las 11:45
    elif (hora_reloj == 11 and min_reloj >= 45) or (hora_reloj == 12 and min_reloj < 20):
        db.detectar_ausencias_automaticas(dia_actual, 4)

    # 5ª Hora (12:20 - 13:10) -> Se marca ausencia a las 12:35
    elif (hora_reloj == 12 and min_reloj >= 35) or (hora_reloj == 13 and min_reloj < 10):
        db.detectar_ausencias_automaticas(dia_actual, 5)

    # 6ª Hora (13:10 - 14:00) -> Se marca ausencia a las 13:25
    elif (hora_reloj == 13 and min_reloj >= 25) or (hora_reloj == 14 and min_reloj < 0):
        db.detectar_ausencias_automaticas(dia_actual, 6)
    
    filas = db.obtener_ausencias_con_datos_profesor(dia_actual)
    guardias_db = db.obtener_guardias_con_nombre_cubre()
    asignadas = {(g[0], g[1]): {'cubre': g[2]} for g in guardias_db}

    sustitutos_por_hora = {}
    for f in filas:
        hora_ausencia = f[0]
        if hora_ausencia not in sustitutos_por_hora:
            sustitutos_por_hora[hora_ausencia] = obtener_ranking_sustitutos(dia_actual, hora_ausencia)

    return render_template(
        "guardias.html",
        filas=filas,
        sustitutos_por_hora=sustitutos_por_hora,
        asignadas=asignadas,
        fecha_actual=fecha_hoy
    )

@app.route("/registrar", methods=["POST"])
def registrar_guardia():
    mensaje = procesar_guardia(
        int(request.form["id_profesor_ausente"]),
        int(request.form["id_profesor_cubre"]),
        request.form["fecha"],
        request.form["hora"],
        request.form["aula"]
    )
    
    flash(mensaje) 
    
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
    profesor_id = int(request.form["profesor_id"])
    dia_actual = datetime.now().isoweekday()
    
    if lector_rfid is not None:
        try:
            print("Lector RFID activo. Esperando tarjeta...")
            id_tarjeta, texto = lector_rfid.read() 
            
            if id_tarjeta: 
                db.gestionar_fichaje_toggle(profesor_id, dia_actual)
                flash("Identificación RFID correcta. Estado actualizado.", "success")
            else:
                flash("Tarjeta RFID no reconocida o no asociada a este profesor.", "danger")
        except Exception as e:
            flash(f"Error físico en el lector de hardware: {e}", "danger")
    else:
        db.gestionar_fichaje_toggle(profesor_id, dia_actual)
        flash("Aviso: Hardware RFID no detectado (Ejecutando en modo local). Estado actualizado.", "warning")
        
    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)