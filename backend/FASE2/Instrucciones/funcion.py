from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion
from FASE2.Symbol.generador import Generador


class Funcion(Abstract):

    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, parametros, sentancias):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias: Abstract = sentancias
        self.parametros = parametros
        self.tipo_secundario = tipo_secundario

    def __str__(self):
        return f"Funcion: {self.id}, tipo: {self.tipo}, tipo_secundario: {self.tipo_secundario}, parametros: {self.parametros}"

    def ejecutar(self, scope):
        if self.sentencias != None:
            result = self.sentencias.ejecutar(scope)
            if self.validacion_salida_funccion(result):
                val = {"value": result['value'], "tipo": result['tipo'],
                       "tipo_secundario": result['tipo_secundario'], "linea": self.linea, "columna": self.columna}
                print(f'Funcion -> {self.id} retorna -> ', val)
                return val
            else:
                val = {"value": None, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario,
                       "linea": self.linea, "columna": self.columna}
                print(f'Funcion -> {self.id} retorna -> ', val)
                return val
        else:
            val = {"value": None, "tipo": self.tipo, "tipo_secundario": self.tipo_secundario,
                   "linea": self.linea, "columna": self.columna}
            print(f'Funcion -> {self.id} retorna -> ', val)
            return val

    def validacion_salida_funccion(self, result: dict) -> bool:
        if result == None:
            return False
        tipo: TipoEnum = result['tipo']
        if (self.tipo == tipo):
            tipo_secundario = result['tipo_secundario']
            if self.tipo == TipoEnum.ARRAY or self.tipo == TipoEnum.STRUCT:
                if tipo_secundario == self.tipo_secundario:
                    return True
                else:
                    self.resultado.add_error(
                        'Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    print(
                        'Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    return False
            else:
                return True
        elif self.tipo == TipoEnum.ANY:
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            print(
                'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            return False

    def graficar(self, graphviz, padre):
        pass

    def generar_c3d(self, scope: Scope):
        print('Estoy compilando funcion ->', scope)
        try:
            scope.declarar_funcion(self.id, self)
            self.compilacion_funcion(scope)
        except ValueError as e:
            self.resultado.add_error(
                'Semantico', str(e), self.linea, self.columna)

    def compilacion_funcion(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        # Generamos el nuevo entorno para la intrucciones de la funcion
        new_scope_func: Scope = Scope(scope)
        # Generacion de la label de retorno para las funciones
        lbl_return = generador.new_label()
        new_scope_func.add_return_label(lbl_return)
        new_scope_func.size = 1

        if self.parametros != None:
            for parametro in self.parametros:
                new_scope_func.declarar_variable(
                    parametro.id, None, parametro.tipo, parametro.tipo_secundario, parametro.tipo == TipoEnum.ANY, self.linea, self.columna)
                new_scope_func.sum_size()
                # TODO: debemos de buscar si la variable es tipo estruct y mandar a llamar sus valores

        generador.add_begin_func(self.id)
        generador.add_comment(f'Compilacion de la funcion {self.id}')
        # Generamos un scope solo para las intrucciones que se ejecutan
        new_inner_scope: Scope = Scope(new_scope_func)
        if self.sentencias != None:
            ret = self.sentencias.generar_c3d(new_inner_scope)
            if isinstance(ret, Excepcion):
                print(ret)

        generador.add_goto(lbl_return)
        generador.put_label(lbl_return)
        generador.add_comment(f'Fin de la compilacion de la funcion {self.id}')
        generador.add_end_func()
        generador.add_space()
