from Abstract.abstract import Abstract


class Detener(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def __str__(self):
        return "Break"

    def ejecutar(self, scope) -> any:
        return None

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Detener"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
