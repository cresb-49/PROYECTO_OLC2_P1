from Abstract.abstract import Abstract


class Retornar(Abstract):
    def __init__(self, resultado,linea, columna, exprecion):
        super().__init__(resultado,linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Return -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        valor = self.exprecion.ejecutar(scope)
        return valor

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('return', padre)
        if self.exprecion != None:
            self.exprecion.ejecutar(graphviz,padre)
