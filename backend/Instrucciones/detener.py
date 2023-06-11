from Abstract.abstract import Abstract


class Detener(Abstract):
    def __init__(self, resultado, linea, columna):
        super().__init__(resultado, linea, columna)

    def __str__(self):
        return f"Break -> linea: {self.linea} ,columna: {self.columna}"

    def ejecutar(self, scope) -> any:
        return self

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('break', padre)
