from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

api = "http://127.0.0.1:8700/v1/usuarios/"

@app.route("/")
def index():
    response = requests.get(api)
    if response.status_code == 200:
        usuarios = response.json().get("data", [])
    else:
        usuarios = []
    return render_template("Usuarios.html", usuarios=usuarios)

@app.route("/agregar", methods=["POST"])
def agregar_usuario():
    nombre = request.form.get("nombre")
    edad = request.form.get("edad")
    id_usuario = request.form.get("id")
        
    try:
        edad = int(edad)
        id_usuario = int(id_usuario)
    except ValueError:
        return "El ID y la edad deben ser números", 400
    
    if id_usuario <= 0:
        return "El ID debe ser un número positivo", 400

    if edad <= 1 or edad > 121:
        return "La edad debe ser un número positivo entre 0 y 121", 400
    
    response = requests.get(api)
    if response.status_code == 200:
        usuarios = response.json().get("data", [])
        if any(usuario["id"] == id_usuario for usuario in usuarios):
            return "El ID ya está ocupado", 400

    usuario = {"id": id_usuario, "nombre": nombre, "edad": edad}
    response = requests.post(api, json=usuario)
    
    if response.status_code == 200:
        return redirect(url_for("index"))
    
    return f"Error al agregar usuario: {response.text}", 400

@app.route("/eliminar", methods=["POST"])
def eliminar_usuario():
    usuario_id = request.form.get("id")
    
    if usuario_id:
        response = requests.delete(f"{api}{usuario_id}")
        
        if response.status_code == 200:
            return redirect(url_for("index"))
        else:
            return "Error al eliminar el usuario. Puede que no exista.", 400
    return "Error: ID no proporcionado.", 400

if __name__ == "__main__":
    app.run(debug=True, port=8600)