from Abstract.abstract import Abstract


class Imprimir(Abstract):
    def __init__(self, resultado,linea, columna, exprecion):
        super().__init__(resultado,linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Print -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        resultado = self.exprecion.ejecutar(scope)
        print(resultado)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>DibujarEXP"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
