from flask import Flask, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/compile', methods=["POST"])
def compile():


    user = request.args.get('codigo')
    print(user)
    return {'s': 'xd'}


@app.route('/saludo', methods=["GET"])
def saludo():
    return {'s': 'xd'}


if __name__ == '__main__':
    app.run(debug=True, port=3000)
