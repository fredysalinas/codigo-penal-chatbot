from flask import Flask, request, render_template
from models import responder_pregunta

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    respuesta = ""
    pregunta = ""
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        respuesta = responder_pregunta(pregunta)
    return render_template("index.html", pregunta=pregunta, respuesta=respuesta)

if __name__ == "__main__":
    app.run(debug=True)