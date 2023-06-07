from Abstract.abstract import Abstract


class Continuar(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def __str__(self):
        return "Continuar"

    def ejecutar(self, scope):
        return None
    
    def graficar(self, scope, graphviz, subNameNode, padre) :
         nume = graphviz.declaraciones.length + 1
         node = "nodo_" + subNameNode + "_" + nume
         decl = node + '[label = "<n>Continuar"];'
         graphviz.declaraciones.push(decl)
         graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
    
