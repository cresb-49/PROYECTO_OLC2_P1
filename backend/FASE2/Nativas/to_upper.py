from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion

class ToUpperCase(Abstract):

    def __init__(self, resultado, linea, columna, cadena):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRING
        self.cadena = cadena

    def __str__(self):
        return "toUpperCase"

    def verificarTipos(self, val):
        # extremos el tipo de la variable
        tipo = val["tipo"]
        if (tipo == TipoEnum.STRING):
            return True
        else:
            concat = f'Tipos no coinciden para la operacion split(), Se esperaba String y recibio {tipo.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)
            return False

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.cadena.ejecutar(scope)
        # una vez traida la variable debemos verificar que se trata d eun string
        if (self.verificarTipos(ejecutar)):
            # mandmaos ha hacer concat sobre el atributo value
            toString = FuncionNativa.hacer_to_upper_case(None, '')
            # retornamos un diccionario con la String en lower y el tipo String
            return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.cadena.graficar(graphviz, result)
        graphviz.add_nodo("toUpperCase", result)

    def generar_c3d(self, scope):
        # mandamos ha traer el c3d de las expreciones que componen el fixed
        c3d_numero:Return = self.cadena.generar_c3d(scope)
        if(isinstance(c3d_numero, Excepcion)):
            return c3d_numero
        generador_aux = Generador()
        generador = generador_aux.get_instance()

        generador.to_upper()
        temporal_parametro = generador.add_temp()
        generador.add_exp(temporal_parametro, 'P', scope.size, '+')
        generador.add_exp(temporal_parametro, temporal_parametro, '1', '+')

        generador.set_stack(temporal_parametro, c3d_numero.get_value())

        generador.new_env(scope.size)
        generador.call_fun("toUpperCase")

        temporal1 = generador.add_temp()
        temporal2 = generador.add_temp()

        generador.add_exp(temporal2, 'P', '1', '+')
        generador.get_stack(temporal1, temporal2)

        return Return(temporal1, TipoEnum.STRING, True, None)
