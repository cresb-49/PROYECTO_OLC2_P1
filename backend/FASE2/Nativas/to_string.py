from FASE2.Abstract.abstract import Abstract
from FASE2.Modulos.funcion_nativa import FuncionNativa
from FASE2.Symbol.tipoEnum import TipoEnum

from FASE2.Abstract.return__ import Return
from FASE2.Symbol.Exception import Excepcion
from FASE2.Symbol.generador import Generador


class ToString(Abstract):

    def __init__(self, resultado, linea, columna, numero):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRING
        self.numero = numero

    def __str__(self):
        return "toString"

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.numero.ejecutar(scope)
        # mandmaos ha hacer concat sobre el atributo value
        toString = FuncionNativa.hacer_to_string(None, ejecutar['value'])
        # retornamos un diccionario con la String realizada y el tipo String
        return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo(".", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
        graphviz.add_nodo("toString", result)

    def generar_c3d(self, scope):
        # declaracion de un nuevo generador de c3d
        generador_aux = Generador()
        generador = generador_aux.get_instance()

        # ejecutamos el diccionario para poder obtener el tipo de dato que se desea convertir ha String
        ejecutar = self.numero.ejecutar(scope)
        # mandamos ha traer el c3d de la variable a converitir a String
        a_convertir: Return = self.numero.generar_c3d(scope)

        if (ejecutar['tipo'] == TipoEnum.ARRAY):
            pass
        elif (ejecutar['tipo'] == TipoEnum.NUMBER):
            return self.to_string_number(generador, a_convertir, scope)
        elif (ejecutar['tipo'] == TipoEnum.BOOLEAN):
            return self.to_string_boolean(generador, a_convertir, scope)
        elif (ejecutar['tipo'] == TipoEnum.STRING):
            return self.to_string_string(generador, a_convertir, scope)
        elif (ejecutar['tipo'] == TipoEnum.ANY):
            if (ejecutar['tipo_secundario'] == TipoEnum.NUMBER):
                return self.to_string_number(generador, a_convertir, scope)
            elif (ejecutar['tipo_secundario'] == TipoEnum.BOOLEAN):
                return self.to_string_boolean(generador, a_convertir, scope)
            elif (ejecutar['tipo_secundario'] == TipoEnum.STRING):
                return self.to_string_string(generador, a_convertir, scope)
        elif (ejecutar['tipo'] == TipoEnum.STRUCT):
            pass

    def to_string_number(self, generador: Generador, a_convertir: Return, scope):
        # # envihamos ha generar la funcion de sumas
        # generador.to_string_number()
        # # generamos el primer temporal
        # param_temp = generador.add_temp()
        # generador.add_exp(param_temp, 'P', scope.size, '+')
        # generador.add_exp(param_temp, param_temp, '1', '+')
        # generador.set_stack(param_temp, a_convertir.get_value())

        # # asignamos el segundo valor a la posicion 3 del stack
        # generador.add_exp(param_temp, param_temp, '1', '+')
        # generador.set_stack(param_temp, a_convertir.get_value())

        # # generar un nuevo entorno
        # generador.new_env(scope.size)
        # # llamamos a la funcion de sumar strings
        # generador.call_fun("to_string_number")

        # # anadir un nuevo temporal que guardara el stack en P
        # temp = generador.add_temp()
        # generador.get_stack(temp, 'P')
        # # retornamos el un entorno
        # generador.ret_env(scope.size)

        # generador.add_comment('Fin de toString()')
        # generador.add_space()

        return Excepcion("Semantico", "Existe la funcion ToString en numeros", self.linea, self.columna)


    def to_string_string(self, generador: Generador, a_convertir: Return, scope):
        # mandamos ha llamar la funcion to String en su version String
        generador.to_string_string()
        temporal_parametro = generador.add_temp()
        generador.add_exp(temporal_parametro, 'P', scope.size, '+')
        generador.add_exp(temporal_parametro, temporal_parametro, '1', '+')

        generador.set_stack(temporal_parametro, a_convertir.get_value())

        generador.new_env(scope.size)
        generador.call_fun("to_string_string")


        temp = generador.add_temp()
        generador.get_stack(temp,'P')
        generador.ret_env(scope.size)



        # retornamos el un entorno
        generador.ret_env(scope.size)

        return Return(temp, TipoEnum.STRING, True, None)

    def to_string_boolean(self, generador: Generador, a_convertir: Return, scope):

        # mandamos ha llamar la funcion to String en su version String
        temp_lbl = generador.new_label()
        for label in a_convertir.get_true_lbls():
            generador.put_label(label)
        generador.new_env(scope.size)
        # guardamos el incio de la nueva cadena
        generador.add_comment(
            "INICIO DE LA NUEVA CADENA")
        t1 = generador.add_temp()
        #escribimos en el heap la palabra true avanzando 1 a uno las posciones en el heap
        generador.add_asig(t1, 'H')
        generador.add_ident()
        generador.set_heap('H', '116')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '114')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '117')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '101')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.add_goto(temp_lbl)
        for label in a_convertir.get_false_lbls():
            generador.put_label(label)
        generador.new_env(scope.size)
        # guardamos el incio de la nueva cadena
        generador.add_comment(
            "INICIO DE LA NUEVA CADENA")
        t1 = generador.add_temp()
        generador.add_asig(t1, 'H')
        #escribimos en el heap la palabra false avanzando 1 a uno las posciones en el heap
        generador.add_ident()
        generador.set_heap('H', '102')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '97')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '108')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '115')
        generador.add_ident()
        generador.next_heap()
        generador.add_ident()
        generador.set_heap('H', '101')
        generador.add_ident()
        generador.next_heap()
        generador.put_label(temp_lbl)



        # anadimos el caracter -1 a la nueva cadena
        generador.set_heap('H', '-1')
        # aumentamos en uno el heap
        generador.next_heap()

        # devolvemos la posicion inicial de la cadena
        generador.set_stack('P', t1)

  
        temp = generador.add_temp()
        generador.get_stack(temp,'P')
        generador.ret_env(scope.size)

        return Return(temp, TipoEnum.STRING, True, None)
