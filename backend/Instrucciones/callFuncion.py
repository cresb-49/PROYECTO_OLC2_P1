from Abstract.abstract import Abstract


class CallFuncion(Abstract):
    def __init__(self,resultado,linea, columna, id, parametros):
        super().__init__(resultado,linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"Llamar Funcion: {self.id}, Parámetros: {self.parametros}"

    def ejecutar(self, scope):
        fun = scope.obtener_funcion(self.id)
        #if (function != None):
        #    fun.ejecutar(scope)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        self.parametros.graficar(graphviz,padre)
        graphviz.add_nodo(')', padre)
