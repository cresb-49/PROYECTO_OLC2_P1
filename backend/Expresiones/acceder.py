from Abstract.abstract import Abstract


class Acceder(Abstract):
    def __init__(self, linea, columna, id):
        super().__init__(linea, columna)
        self.id = id

    def ejecutar(self, scope):
        recuperacion = scope.obtenerVariable(self.id)
        if (recuperacion == None):
            raise ValueError("La variable", self.identificador,
                             "no existe, Linea: ", self.linea, " ,Columna: ", self.columna)
        return recuperacion

    def graficar(self, scope, graphviz, subNameNode, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + ' [label="<f0> ID |<f1> ' + self.id + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)
