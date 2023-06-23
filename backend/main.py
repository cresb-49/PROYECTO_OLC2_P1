from flask import Flask, request
import json
from flask_cors import CORS
from FASE1.principal_api_fase1 import PrincipalFase1
from FASE2.principal_api_fase2 import PrincipalFase2
import sys

sys.setrecursionlimit(10000000)
app = Flask(__name__)
CORS(app)


@app.route('/compile', methods=["POST"])
def compile():

    principal = PrincipalFase1()

    codigo = request.json.get('codigo')

    # enviamos ha compilar el codigo que se envio
    compilacion = principal.leer(codigo)

    # objeto que enviaremos ha convertir a json
    convertir_a_json = {
        'consola': compilacion['result'].consola,
        'errores': [p.__dict__ for p in compilacion['result'].errores],
        'dot': compilacion['dot'],
        'simbolos':  compilacion['simbolos']
    }

    json2 = json.dumps(convertir_a_json)
    return json2


@app.route('/compile2', methods=["POST"])
def compile2():

    principal2 = PrincipalFase2()

    codigo = request.json.get('codigo')

    # enviamos ha compilar el codigo que se envio
    compilacion = principal2.leer(codigo)

    # objeto que enviaremos ha convertir a json
    convertir_a_json = {
        'errores': [p.__dict__ for p in compilacion['result'].errores],
        'c3d': compilacion['c3d']
    }

    json2 = json.dumps(convertir_a_json)
    return json2


if __name__ == '__main__':
    app.run(debug=True, port=3000)
