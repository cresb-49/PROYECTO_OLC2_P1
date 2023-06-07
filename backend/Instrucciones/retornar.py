from Abstract.abstract import Abstract


class Retornar(Abstract):
    def __init__(self, linea, columna, exprecion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Return -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        valor = self.exprecion.ejecutar(scope)
        return valor

    def graficar(scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Retorno"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        nume2 = graphviz.declaraciones.length + 1
        node2 = "nodo_" + subNameNode + "_" + nume2
        decl2 = node2 + '[label = "<n>Exprecion"];'
        graphviz.declaraciones.push(decl2)
        graphviz.relaciones.push((node + ':n -> ' + node2 + ':n'))
