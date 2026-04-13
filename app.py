from flask import Flask
from modules.guardias.models import Guardia
from modules.guardias.motor import procesar_entrada

app = Flask(__name__)

@app.route("/")
def home():
    g = Guardia(1, "Juan")
    return procesar_entrada(g)

if __name__ == "__main__":
    app.run(debug=True)