from Retorno import Retorno
from Simbolo.Scope import Scope


class Expresion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    def ejecutar(self, scope: Scope) -> Retorno:
        print(scope)
        return None

    def graficar(self, scope, graphviz, padre):
        print(scope, graphviz, padre)
        return None
