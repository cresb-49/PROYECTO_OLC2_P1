from Abstract.abstract import Abstract


class CallFuncion(Abstract):
    def __init__(self, resultado, linea, columna, id, parametros):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"Llamar Funcion: {self.id}, Parámetros: {self.parametros}"

    def ejecutar(self, scope):
        fun = scope.obtener_funcion(self.id)
        if fun != None:
            if self.parametros == None:
                # Ejecucion de funcion sin parametros
                # Debemos de mandar el scope global
                resultado = fun.ejecutar(None)
                if isinstance(resultado, dict):
                    print(resultado)
            else:
                # Ejecucion de una funcion con parametros
                print('Ejecucion de funcion con parametros', type(fun))
        else:
            print('Se invoco un funcion que no esta definida')

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        self.parametros.graficar(graphviz, padre)
        graphviz.add_nodo(')', padre)
