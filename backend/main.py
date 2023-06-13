from flask import Flask, request
import json
from flask_cors import CORS
import principal_api

app = Flask(__name__)
CORS(app)


@app.route('/compile', methods=["POST"])
def compile():
    codigo = request.json.get('codigo')

    #enviamos ha compilar el codigo que se envio
    compilacion = principal_api.leer(codigo)

    #objeto que enviaremos ha convertir a json
    convertir_a_json = {
        'consola': compilacion['result'].consola,
        'errores': [p.__dict__ for p in compilacion['result'].errores],
        'dot': compilacion['dot'],
    }

    json2 = json.dumps(convertir_a_json)
    return json2


if __name__ == '__main__':
    app.run(debug=True, port=3000)
