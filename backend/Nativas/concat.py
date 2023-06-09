from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa

class Concat(Abstract):
    def __init__(self, resultado,linea, columna,array1, array2):
        super().__init__(resultado,linea, columna)
        self.array1 = array1
        self.array2 = array2

    def __str__(self):
        return "Concat"

    def ejecutar(self, scope):
        return FuncionNativa.hacer_concat(self.array1, self.array2)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Concat"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
