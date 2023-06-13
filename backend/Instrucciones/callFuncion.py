from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Instrucciones.funcion import Funcion
import traceback


class CallFuncion(Abstract):
    def __init__(self, resultado, linea, columna, id, parametros):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"Llamar Funcion: {self.id}, Parámetros: {self.parametros}"

    def ejecutar(self, scope):
        codigo_referencia = str(id(self))
        fun = scope.obtener_funcion(self.id)
        if fun != None and isinstance(fun, Funcion):
            size = 0
            size_funcion = 0
            if self.parametros != None:
                size = len(self.parametros)

            if fun.parametros != None:
                size_funcion = len(fun.parametros)
            if size_funcion == size:
                if self.parametros == None:
                    # Ejecucion de funcion sin parametros
                    # Declaramos scope de tranajo pero debemos mandar el scope
                    scope_funcion: Scope = Scope(self.resultado.get_scope_global())
                    # Registro del entorno generado 
                    self.resultado.agregar_entorno(codigo_referencia,scope_funcion)
                    resultado = fun.ejecutar(scope_funcion)
                    if isinstance(resultado, dict):
                        print(resultado)
                        return resultado
                else:
                    # Ejecucion de una funcion con parametros
                    # Declaracion del scope de trabajo
                    scope_funcion: Scope = Scope(self.resultado.get_scope_global())
                    # Registro del entorno generado 
                    self.resultado.agregar_entorno(codigo_referencia,scope_funcion)
                    try:
                        # Hacemos la declaracion de variables en el scope de la funcion
                        if fun.parametros != None:
                            for param_fun, param_send in zip(fun.parametros, self.parametros):
                                param_fun.valor = param_send
                                param_fun.ejecutar(scope_funcion)
                        # Ejecutamos la funcion si retornar ningun valor
                        fun.ejecutar(scope_funcion)
                    except Exception as e:
                        print(
                            'Semantico', f'Error al ejecutar la funcion {str(e)}', self.linea, self.columna)
                        self.resultado.add_error(
                            'Semantico', f'Error al ejecutar la funcion {str(e)}', self.linea, self.columna)
                        traceback.print_exc()
            else:
                self.resultado.add_error(
                    'Semantico', f'La funcion que desea ejecutar necesita {size_funcion} parametros, pero la esta ejecutando con {size} parametros', self.linea, self.columna)
        else:
            self.resultado.add_error(
                'Semantico', 'Esta invocando un funcion que no existe en el programa', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        self.parametros.graficar(graphviz, padre)
        graphviz.add_nodo(')', padre)
