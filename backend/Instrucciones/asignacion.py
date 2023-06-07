from Abstract.abstract import Abstract


class Asignacion(Abstract):
    def __init__(self, linea, columna, id, valor):
        super().__init__(linea, columna)
        self.id = id
        self.valor = valor

    def __str__(self):
        return f"Asignacion: {self.id}, Valor: {self.valor}"

    def ejecutar(self, scope):
        result = self.valor.ejecutar(scope)
        #tipo_secundario = None
        #modificar_variable(self.id, result.value, tipo_secundario):

    def graficar(self, scope, graphviz, subNameNode, padre) :
         nume = graphviz.declaraciones.length + 1
         node = "nodo_" + subNameNode + "_" + nume
         decl = node + '[label = "<n>Asignacion"];'
         graphviz.declaraciones.push(decl)
         graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
         nume2 = graphviz.declaraciones.length + 1
         node2 = "nodo_" + subNameNode + "_" + nume2
         decl2 = node2 + '[label = "<n>Exprecion"];'
         graphviz.declaraciones.push(decl2)
         graphviz.relaciones.push((node + ':n -> ' + node2 + ':n'))
