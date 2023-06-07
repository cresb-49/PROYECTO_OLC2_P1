from Abstract.abstract import Abstract


class CallFuncion(Abstract):
    def __init__(self, linea, columna, id, parametros):
        super().__init__(linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"Llamar Funcion: {self.id}, Parámetros: {self.parametros}"

    def ejecutar(self, scope):
        fun = scope.obtener_funcion(self.id)
        if (function != None):
            fun.ejecutar(scope)
