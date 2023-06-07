from Abstract.abstract import Abstract


class Mientras(Abstract):
    def __init__(self, linea, columna, condicion, sentencias):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def __str__(self):
        return f"While -> Condición: {self.condicion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        condicion = self.condicion.ejecutar(scope)
    

    def  graficar(self, scope, graphviz, subNameNode, padre) :
         nume = graphviz.declaraciones.length + 1
         node = "nodo_" + subNameNode + "_" + nume
         decl = node + '[label = "<n>Mientras"];'
         graphviz.declaraciones.push(decl)
         graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))   
         self.sentencias.graficar(scope,graphviz,subNameNode,node)
    
