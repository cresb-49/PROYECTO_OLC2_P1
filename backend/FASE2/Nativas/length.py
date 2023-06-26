from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum

from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion
from FASE2.Symbol.generador import Generador
from FASE2.Expresiones.acceder_array import AccederArray
from FASE2.Expresiones.acceder import Acceder


class Length(Abstract):
    def __init__(self, resultado, linea, columna, acceder):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.NUMBER
        self.acceder = acceder

    def __str__(self):
        return "length"

    def validar_tipos(self, tipo_exprecion):
        # si se trata de una suma debemos verificar que los dos tipos sean iguales y sean string o number
        if (tipo_exprecion == TipoEnum.STRING or tipo_exprecion == TipoEnum.ARRAY):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'Tipos no coinciden para la operacion length , Se esperaba String | Array y se recibio {tipo_exprecion}', self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        return {"value": None, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar os hijos
        self.acceder[0].graficar(graphviz, result)
        graphviz.add_nodo("length", result)

    def generar_c3d(self, scope):
        # declaracion de un nuevo generador de c3d
        generador_aux = Generador()
        generador = generador_aux.get_instance()

        # mandamos ha traer el c3d de las expreciones que componen el fixed
        c3d_numero: Return = self.acceder[0].generar_c3d(scope)
        if (isinstance(c3d_numero, Excepcion)):
            return c3d_numero
        if (isinstance(self.acceder[0], AccederArray)):
            acceder = Acceder(self.resultado, self.linea, self.columna, self.acceder[0].exprecion.id)
            c3d_acceder = acceder.generar_c3d(scope)
            return self.generar_c3d_array_de_array(scope, generador, c3d_acceder)
        elif (c3d_numero.get_tipo() == TipoEnum.ARRAY):
            return self.generar_c3d_array(scope, generador, c3d_numero)
        else:
            # mandamos ha construir la funcion length
            generador.length()

            temporal_parametro = generador.add_temp()
            generador.add_exp(temporal_parametro, 'P', scope.size, '+')
            generador.add_exp(temporal_parametro, temporal_parametro, '1', '+')

            generador.set_stack(temporal_parametro, c3d_numero.get_value())

            generador.new_env(scope.size)
            # llamamos a la funcion length
            generador.call_fun("length")

            # anadir un nuevo temporal que guardara el stack en P
            temp = generador.add_temp()
            generador.get_stack(temp, 'P')
            # retornamos un entorno
            generador.ret_env(scope.size)

            generador.add_comment('Fin del length')
            generador.add_space()

            return Return(temp, TipoEnum.NUMBER, True, None)

    def generar_c3d_array(self, scope, generador: Generador, a_convertir):
        # mandamos ha construir la funcion length_of_array
        generador.length_of_array()

        temporal_parametro = generador.add_temp()
        generador.add_exp(temporal_parametro, 'P', scope.size, '+')
        generador.add_exp(temporal_parametro, temporal_parametro, '1', '+')

        generador.set_stack(temporal_parametro, a_convertir.get_value())

        generador.new_env(scope.size)
        # llamamos a la funcion length
        generador.call_fun("length_of_array")

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin del length')
        generador.add_space()

        return Return(temp, TipoEnum.NUMBER, True, None)

    def generar_c3d_array_de_array(self, scope, generador: Generador, a_convertir):

        for x in self.acceder[0].list_index_exprecion:
            print("----------->", x)
        # mandamos ha construir la funcion length_of_array
        generador.length_of_array_dimension()

        temporal_parametro = generador.add_temp()

        generador.add_exp(temporal_parametro, 'P', scope.size, '+')
        generador.add_exp(temporal_parametro, temporal_parametro, '1', '+')

        generador.set_stack(temporal_parametro, a_convertir.get_value())

        parametro_zice = generador.add_temp()

        # guardamos el segundo parametro una pocion despues del
        generador.add_exp(parametro_zice, temporal_parametro, '1', '+')

        generador.set_stack(parametro_zice, len(
            self.acceder[0].list_index_exprecion))

        generador.new_env(scope.size)
        # llamamos a la funcion length
        generador.call_fun("length_of_array_dimension")

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin del xxxx')
        generador.add_space()

        return Return(temp, TipoEnum.NUMBER, True, None)
