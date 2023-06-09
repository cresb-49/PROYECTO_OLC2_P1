from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Instrucciones.funcion import Funcion


class CallFuncion(Abstract):
    def __init__(self, resultado, linea, columna, id, parametros):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"Llamar Funcion: {self.id}, Parámetros: {self.parametros}"

    def ejecutar(self, scope):
        fun = scope.obtener_funcion(self.id)
        if fun != None and isinstance(fun, Funcion):
            size = 0
            size_funcion = 0
            if self.parametros != None:
                size = len(self.parametros)

            if fun.parametros != None:
                size_funcion = len(fun.parametros)
            # print(size_funcion)
            # print(size)
            if size_funcion == size:
                if self.parametros == None:
                    # Ejecucion de funcion sin parametros
                    # Declaramos scope de tranajo pero debemos mandar el scope
                    scope_global = None
                    scope_funcion: Scope = Scope(scope_global)
                    resultado = fun.ejecutar(scope_funcion)
                    if isinstance(resultado, dict):
                        print(resultado)
                        return resultado
                else:
                    # Ejecucion de una funcion con parametros
                    # Declaracion del scope de trabajo
                    scope_global = None
                    scope_funcion: Scope = Scope(scope_global)
                    try:
                        # Hacemos la declaracion de variables en el scope de la funcion
                        for param_fun, param_send in zip(fun.parametros, self.parametros):
                            param_fun.valor = param_send
                            param_fun.ejecutar(scope_funcion)                        
                        resultado = fun.ejecutar(scope_funcion)
                        if isinstance(resultado, dict):
                            print(resultado)
                            return resultado
                        
                    except Exception as e:
                        print('Error'+str(e))
            else:
                print(
                    f'La funcion que desea ejecutar necesita {size_funcion} parametros, pero la esta ejecutando con {size} parametros')
        else:
            print('Se invoco un funcion que no esta definida')

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        self.parametros.graficar(graphviz, padre)
        graphviz.add_nodo(')', padre)
