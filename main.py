from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def root():
    return "API funcionando viva cristo rey"


@app.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    user = {"id": user_id, "Name": "El Max", "Status": "Activo", "Telefono": "449-666-6666"}
    query = request.args.get("query")
    if query:
        user["query"] = query
    return jsonify(user), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({"mesaje": "Usuarios Creado ahuevo", "data": data}),201


if __name__ == "__main__":
    app.run()