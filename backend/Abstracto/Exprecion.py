class Expresion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    def ejecutar(self, scope) -> None:
        print(scope)
        return None

    def graficar(self, scope, graphviz, padre) -> None:
        print(scope, graphviz, padre)
        return None
