from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.Exception import Excepcion
from FASE2.Instrucciones.funcion import Funcion
from FASE2.Symbol.tipoEnum import TipoEnum
import traceback


class ValFuncion(Abstract):
    def __init__(self, resultado, linea, columna, id, parametros):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.parametros = parametros

    def __str__(self):
        return f"ValFuncion: {self.id}, Parámetros: {self.parametros}"

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
                    scope_funcion: Scope = Scope(
                        self.resultado.get_scope_global())
                    # Registramos el entorno utilizado
                    self.resultado.agregar_entorno(
                        codigo_referencia, scope_funcion)
                    resultado = fun.ejecutar(scope_funcion)
                    if isinstance(resultado, dict):
                        print(resultado)
                        return resultado
                else:
                    # Ejecucion de una funcion con parametros
                    # Declaracion del scope de trabajo
                    scope_funcion: Scope = Scope(
                        self.resultado.get_scope_global())
                    # Registramos el entorno utilizado
                    self.resultado.agregar_entorno(
                        codigo_referencia, scope_funcion)
                    try:
                        # Hacemos la declaracion de variables en el scope de la funcion
                        if fun.parametros != None:
                            for param_fun, param_send in zip(fun.parametros, self.parametros):
                                param_fun.ejecutar(scope_funcion)
                                result = param_send.ejecutar(scope)
                                self.asignacion_valor_funcion(
                                    param_fun.id, scope_funcion, result)
                        scope_funcion.imprimir()
                        value = fun.ejecutar(scope_funcion)
                        return value
                    except Exception as e:
                        print(
                            'Semantico', f'Error al ejecutar la funcion {str(e)}', self.linea, self.columna)
                        self.resultado.add_error(
                            'Semantico', f'Error al ejecutar la funcion {str(e)}', self.linea, self.columna)
                        traceback.print_exc()
            else:
                self.resultado.add_error(
                    'Semantico', f'La funcion que desea ejecutar necesita {size_funcion} parametros, pero la esta ejecutando con {size} parametros', self.linea, self.columna)
                print(
                    'Semantico', f'La funcion que desea ejecutar necesita {size_funcion} parametros, pero la esta ejecutando con {size} parametros', self.linea, self.columna)
        else:
            print('Semantico', 'Esta invocando un funcion que no existe en el programa',
                  self.linea, self.columna)
            self.resultado.add_error(
                'Semantico', 'Esta invocando un funcion que no existe en el programa', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('function', padre)
        graphviz.add_nodo(self.id, result)
        node_params = graphviz.add_nodo('params', result)
        # si los parametros no son nulos entonces mandamos ha graficar
        if (self.parametros != None):
            for nodo in self.parametros:
                nodo.graficar(graphviz, node_params)

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

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        funcion = scope.obtener_funcion(self.id)
        if funcion == None:
            self.resultado.add_error(
                'Semantico', f'La funcion "{self.id}" no esta definida en el programa', self.columna, self.columna)
            return Excepcion('Semantico', f'La funcion "{self.id}" no esta definida en el programa', self.linea, self.columna)

        param_values = []
        tmps = []
        size = scope.size

        for parametros in self.parametros:
            value = parametros.generar_c3d(scope)
            if isinstance(value, Excepcion):
                return value
            param_values.append(value)
            tmps.append(value.get_value())

        temp = generador.add_temp()
        generador.add_exp(temp, 'P', size+1, '+')
        aux = 0
        if len(funcion.parametros) == len(param_values):
            for param_fun, param_send in zip(funcion.parametros, param_values):
                if param_fun.tipo == param_send.type:
                    print('debuj1 val_funcion =>', param_fun)
                    print('debuj2 val_funcion =>', param_send)
                    aux += 1
                    generador.set_stack(temp, param_send.get_value())
                    if aux != len(param_values):
                        generador.add_exp(temp, temp, 1, '+')
                else:
                    self.resultado.add_error(
                        'Semantico', f'Esta asignando un valor de tipo {param_send.type.value} a un parametro de tipo {param_fun.tipo.value}', self.columna, self.columna)
                    return Excepcion('Semantico', f'Esta asignando un valor de tipo {param_send.type.value} a un parametro de tipo {param_fun.tipo.value}', self.linea, self.columna)
            generador.new_env(size)
            generador.call_fun(self.id)
            generador.get_stack(temp, 'P')
            generador.ret_env(size)
            generador.add_comment(f'Fin de la llamada a la funcion {self.id}')
            generador.add_space()
            if funcion.tipo != TipoEnum.BOOLEAN:
                return Return(temp, funcion.tipo, True, None)
            else:
                generador.add_comment('Recuperacion de booleano')
                if self.true_lbl == '':
                    self.true_lbl = generador.generator.new_label()
                if self.false_lbl == '':
                    self.false_lbl = generador.generator.new_label()
                generador.add_if(temp, 1, '==', self.true_lbl)
                generador.add_goto(self.true_lbl)
                ret = Return(temp, TipoEnum.BOOLEAN, True, None)
                ret.add_true_lbl(self.true_lbl)
                ret.add_false_lbl(self.false_lbl)
                generador.add_comment('Fin de recuperacion de booleano')
                return ret
        else:
            self.resultado.add_error(
                'Semantico', f'No esta enviado la cantidad correcta de parametros a a funcion "{self.id}"', self.columna, self.columna)
            return Excepcion('Semantico', f'No esta enviado la cantidad correcta de parametros a a funcion "{self.id}"', self.linea, self.columna)
