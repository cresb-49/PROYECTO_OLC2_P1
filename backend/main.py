from flask import Flask, request
import json
from flask import jsonify
from flask_cors import CORS
import principal_api

app = Flask(__name__)
CORS(app)


@app.route('/compile', methods=["POST"])
def compile():
    codigo = request.json.get('codigo')

    json2 = json.dumps(principal_api.leer(codigo).__dict__)
    return json2


if __name__ == '__main__':
    app.run(debug=True, port=3000)
