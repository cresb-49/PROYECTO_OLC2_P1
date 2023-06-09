from Abstract.abstract import Abstract


class Funcion(Abstract):

    def __init__(self, resultado, linea, columna, id, tipo, parametros, sentancias):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros

    def __str__(self):
        return f"Funcion: {self.id}, Tipo: {self.tipo}, Parametros: {self.parametros}"

    def ejecutar(self, scope):
        result = self.sentencias.ejecutar(scope)
        return result

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        # TODO: Agregar la imprecion de los parametros
        graphviz.add_nodo('parametros', padre)
        graphviz.add_nodo(')', padre)
        graphviz.add_nodo('{', padre)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, padre)
        graphviz.add_nodo('}', padre)
