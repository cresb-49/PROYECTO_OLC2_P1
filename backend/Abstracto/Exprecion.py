from Retorno import Retorno
from Simbolo.Scope import Scope


class Exprecion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    def ejecutar(self, scope: Scope) -> Retorno:
        print(scope)

    def graficar(self, scope, graphviz, padre):
        print(scope, graphviz, padre)
        return None
