from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import date, datetime
import modules.db.db_manager as db
from modules.guardias.motor import obtener_ranking_sustitutos, procesar_guardia
from modules.presencia.rfid import leer_tarjeta

app = Flask(__name__) # Inicialización de la aplicación Flask
app.secret_key = 'proyecto_guardias_clave_secreta' # Clave secreta para sesiones y flash messages

@app.route("/")
def index():
    """
    Ruta principal del sistema.
    Renderiza la página de inicio del panel de gestión de guardias del IES.
    """
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():
    """
    Controlador de la interfaz web de gestión de ausencias y asignación de guardias.
    Comprueba de manera automatizada las franjas horarias del instituto, calcula
    las ausencias automáticas por inasistencia y obtiene el ranking de sustitutos idóneos.
    """
    ahora = datetime.now()
    dia_actual = datetime.now().isoweekday()
    hora_reloj = ahora.hour
    min_reloj = ahora.minute
    fecha_hoy = date.today().isoformat()
    
    # SISTEMA AUTOMÁTICO DE DETECCIÓN DE AUSENCIAS SEGÚN LA HORA DEL RELOJ

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
    
    filas = db.obtener_ausencias_con_datos_profesor(dia_actual) # Obtiene las ausencias del día actual junto con los datos de los profesores ausentes
    
    # Recupera las guardias ya cubiertas y confirmadas desde la base de datos
    guardias_db = db.obtener_guardias_con_nombre_cubre() 
    asignadas = {(g[0], g[1]): {'cubre': g[2]} for g in guardias_db}

    # Generar el ranking ordenado de profesores sustitutos para cada hora con ausencias
    sustitutos_por_hora = {}
    for f in filas:
        hora_ausencia = f[0]
        if hora_ausencia not in sustitutos_por_hora:
            # Aplico las prioridades en cascada
            sustitutos_por_hora[hora_ausencia] = obtener_ranking_sustitutos(dia_actual, hora_ausencia)

    # Envío todos los datos recopilados e interconectados a la plantilla HTML
    return render_template(
        "guardias.html",
        filas=filas,
        sustitutos_por_hora=sustitutos_por_hora,
        asignadas=asignadas,
        fecha_actual=fecha_hoy
    )

@app.route("/registrar", methods=["POST"])
def registrar_guardia():
    """
    Controlador para procesar el formulario de asignación de una guardia.
    Valida las reglas del negocio llamando a la capa del motor y devuelve una alerta.
    """
    mensaje = procesar_guardia( # Llamada a la función del motor de reglas para procesar la asignación de guardia
        int(request.form["id_profesor_ausente"]),
        int(request.form["id_profesor_cubre"]),
        request.form["fecha"],
        request.form["hora"],
        request.form["aula"]
    )
    
    flash(mensaje) # Almacena el mensaje del resultado en la sesión web para el usuario
    
    return redirect(url_for("vista_guardias"))

@app.route("/eliminar", methods=["POST"])
def eliminar_guardia():
    """
    Controlador para cancelar o eliminar una asignación de guardia existente.
    Redirige a la vista de guardias tras actualizar la base de datos.
    """
    db.eliminar_guardia_por_hora_aula(request.form["hora"], request.form["aula"])
    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    """
    Controlador de la interfaz web para el control diario de presencia.
    Limpia los datos del día anterior y solicita la lista actualizada de estados.
    """
    db.limpiar_tablas_diarias() # Limpia las tablas de ausencias y fichajes del día anterior para empezar fresco cada día
    profesores = db.obtener_estado_presencia_todos()
    return render_template("presencia.html", profesores=profesores)

@app.route("/toggle_presencia", methods=["POST"])
def toggle_presencia():
    """
    Controlador para cambiar el estado de asistencia de un profesor.
    Ahora utiliza el módulo modularizado en modules/presencia/rfid.py
    """
    profesor_id = int(request.form["profesor_id"])
    dia_actual = datetime.now().isoweekday()
    
    # Intentamos leer la tarjeta usando tu nuevo módulo
    id_tarjeta = leer_tarjeta()
    
    if id_tarjeta:
        db.gestionar_fichaje_toggle(profesor_id, dia_actual)
        flash(f"Identificación correcta (ID: {id_tarjeta}). Estado actualizado.", "success")
    else:
        flash("Error: No se ha detectado tarjeta o el lector no responde.", "danger")
        
    return redirect(url_for("vista_presencia"))

if __name__ == "__main__":
    app.run(debug=True)