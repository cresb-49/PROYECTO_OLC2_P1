class Instruccion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    # Funcion base se debe de sobreescibir para las demas clases heredadas
    def ejecutar(self, scope) -> any:
        print(scope)
        return None

    # Funcion base se debe de sobreescibir para las demas clases heredadas
    def graficar(self, scope, graphviz, padre) -> None:
        print(scope, graphviz, padre)
        return None
