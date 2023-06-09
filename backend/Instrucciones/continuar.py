from Abstract.abstract import Abstract


class Continuar(Abstract):
    def __init__(self, resultado,linea, columna):
        super().__init__(resultado,linea, columna)

    def __str__(self):
        return "Continuar"

    def ejecutar(self, scope):
        return None

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('continue', padre)
