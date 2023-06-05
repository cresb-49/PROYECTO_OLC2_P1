class Expresion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    def ejecutar(self, scope) -> None:
        pass

    def graficar(self, scope, graphviz, padre) -> None:
        pass
