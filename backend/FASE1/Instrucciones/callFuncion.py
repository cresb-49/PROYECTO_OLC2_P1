from FASE1.Abstract.abstract import Abstract
from FASE1.Symbol.scope import Scope
from FASE1.Symbol.tipoEnum import TipoEnum
from FASE1.Instrucciones.funcion import Funcion
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
                    fun.ejecutar(scope_funcion)
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
                                param_fun.ejecutar(scope_funcion)
                                result = param_send.ejecutar(scope)
                                self.asignacion_valor_funcion(param_fun.id,scope_funcion,result)
                        scope_funcion.imprimir()
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
        node_funcion = graphviz.add_nodo('Funcion', padre)
        graphviz.add_nodo(self.id, node_funcion)
        node_params = graphviz.add_nodo('Parametros', node_funcion)
        if self.parametros != None:
            for param in self.parametros:
                param.graficar(graphviz,node_params)

    def asignacion_valor_funcion(self, id, scope_funcion, result_exprecion):
        variable_recuperada = scope_funcion.obtener_variable(id)
        if variable_recuperada != None:
            # Verificamos una variable any ya que a esta le debemos cambiar su tipo secundario
            if variable_recuperada.tipo == TipoEnum.ANY:
                variable_recuperada.tipo_secundario = result_exprecion['tipo'].value
                variable_recuperada.valor = result_exprecion['value']
            else:
                # Verificamos que la variable recuperada coincida en tipo como es resultado de la exprecio
                if variable_recuperada.tipo == result_exprecion['tipo']:
                    variable_recuperada.valor = result_exprecion['value']
                else:
                    concat = f"No se puede asignar un: {result_exprecion['tipo'].value}, a la variable: {self.id}: {variable_recuperada.tipo.value} , linea: {self.linea}, columna: {self.columna}"
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
        else:
            concat = 'No se puede encontrar la variable: ', self.id, ', linea: ', self.linea, ', columna: ', self.columna
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)

    def generar_c3d(self,scope):
        pass