from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/sum", methods=["GET"])
def sum():
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    return jsonify({"result": a + b})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    number = data.get("number", type=int)
    if number > 0:
        return jsonify({"message": "okey"})
    else:
        return jsonify({"message": "number must be greater than 0"}), 400

if __name__ == "__main__":
    app.run(port=8080)
