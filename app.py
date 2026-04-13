from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# DATOS SIMULADOS
guardias = {
    "08:00": {
        "aulas": ["Aula 101", "Aula 102"],
        "profesores": ["Ana", "Luis", "Marta"]
    },
    "09:00": {
        "aulas": ["Aula 201"],
        "profesores": ["Carlos", "Elena"]
    }
}

# Contadores simulados
guardias_acumuladas = {}
guardias_semana = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/guardias")
def vista_guardias():
    return render_template("guardias.html", guardias=guardias)

@app.route("/registrar", methods=["POST"])
def registrar_guardia():
    hora = request.form["hora"]
    profesor = request.form["profesor"]

    # actualizar contadores
    guardias_acumuladas[profesor] = guardias_acumuladas.get(profesor, 0) + 1
    guardias_semana[profesor] = guardias_semana.get(profesor, 0) + 1

    return redirect(url_for("vista_guardias"))

@app.route("/presencia")
def vista_presencia():
    return render_template("presencia.html")


if __name__ == "__main__":
    app.run(debug=True)