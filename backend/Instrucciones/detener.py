from Abstract.abstract import Abstract


class Detener(Abstract):
    def __init__(self,resultado, linea, columna):
        super().__init__(resultado,linea, columna)

    def __str__(self):
        return "Break"

    def ejecutar(self, scope) -> any:
        return None

    def graficar(self, graphviz, padre):
        graphviz.add_nodo('break', padre)
