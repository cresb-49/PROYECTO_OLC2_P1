from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion


class TypeOf(Abstract):
    def __init__(self, resultado, linea, columna, expreciones):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRING
        self.expreciones = expreciones

    def __str__(self):
        return "TypeOf"

    def ejecutar(self, scope):

        # Verificar que solo venga un parametro
        if (len(self.expreciones) == 1):
            expresion = self.expreciones[0]
            # Enviar ha ejecutar la exprecion para obtener su diccionario
            ejecutarExpresion = expresion.ejecutar(scope)
            # calor del saparador de split
            tipo = ejecutarExpresion['tipo']
            tipo_secundario = ejecutarExpresion['tipo_secundario']

            if (tipo_secundario != None):
                # si el tipo secundario no es none entonces es un any y devolvemos el valor del tipo secundario
                return {"value": tipo_secundario, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                # si el tipo secundario es non entonces devolvemos el valor del tipo principal
                return {"value": tipo.value, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

        else:
            self.resultado.add_error(
                'Semantico', 'typeof(), no se puede ejecutar con mas de 1 parametro', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("typeOf", padre)
        # mandmaos ha graficar os hijos
        self.expreciones[0].graficar(graphviz, result)

    def generar_c3d(self, scope):
        # mandamos ha traer el c3d de las expreciones que componen el fixed
        c3d_numero: Return = self.expreciones[0].generar_c3d(scope)
        if (isinstance(c3d_numero, Excepcion)):
            return c3d_numero

        # declaracion de un nuevo generador de c3d
        generador_aux = Generador()
        generador = generador_aux.get_instance()

        llamada_funcion = ""
        if (c3d_numero.get_tipo() == TipoEnum.STRING):
            # mandamos ha construir la funcion type_of_string
            generador.type_of_string()
            # llamada funcion sera el nombre de la funcion ha llamar
            llamada_funcion = "type_of_string"
        elif (c3d_numero.get_tipo() == TipoEnum.NUMBER):
            # mandamos ha construir la funcion type_of_number
            generador.type_of_number()
            # llamada funcion sera el nombre de la funcion ha llamar
            llamada_funcion = "type_of_number"
        elif (c3d_numero.get_tipo() == TipoEnum.BOOLEAN):

            return self.type_of_boolean(generador, c3d_numero, scope)

        elif (c3d_numero.get_tipo() == TipoEnum.ARRAY):
            # mandamos ha construir la funcion length
            generador.type_of_string()
            # llamada funcion sera el nombre de la funcion ha llamar
            llamada_funcion = "type_of_boolean"
        elif (c3d_numero.get_tipo() == TipoEnum.STRUCT):
            # mandamos ha construir la funcion length
            generador.type_of_string()
            # llamada funcion sera el nombre de la funcion ha llamar
            llamada_funcion = "type_of_boolean"

        generador.new_env(scope.size)
        # llamamos a la funcion length
        generador.call_fun(llamada_funcion)

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin del type_of')
        generador.add_space()

        return Return(temp, TipoEnum.STRING, True, None)

    def type_of_boolean(self, generador: Generador, a_convertir: Return, scope):
        temp_lbl = generador.new_label()
        for label in a_convertir.get_true_lbls():
            generador.put_label(label)

        generador.add_goto(temp_lbl)
        for label in a_convertir.get_false_lbls():
            generador.put_label(label)
   

        generador.put_label(temp_lbl)
        # mandamos ha construir la funcion type_of_boolean
        generador.type_of_boolean()
        # llamada funcion sera el nombre de la funcion ha llamar
        llamada_funcion = "type_of_boolean"

        generador.new_env(scope.size)
        # llamamos a la funcion length
        generador.call_fun(llamada_funcion)

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin del type_of')
        generador.add_space()

        return Return(temp, TipoEnum.STRING, True, None)
