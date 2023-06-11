from Abstract.abstract import Abstract


class Continuar(Abstract):
    def __init__(self, resultado, linea, columna):
        super().__init__(resultado, linea, columna)

    def __str__(self):
        return f"Continue -> linea: {self.linea} ,columna: {self.columna}"

    def ejecutar(self, scope):
        return self

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('continue', padre)
