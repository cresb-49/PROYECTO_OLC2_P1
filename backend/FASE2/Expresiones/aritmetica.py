from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.Exception import Excepcion
from FASE2.Abstract.return__ import Return
from FASE2.Expresiones.val_funcion import ValFuncion


class Aritmetica(Abstract):
    def __init__(self, resultado, linea, columna, expresion_izquierda, expresion_derecha, tipo_operacion):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.NUMBER
        self.expresion_izquierda = expresion_izquierda
        self.expresion_derecha = expresion_derecha
        self.tipo_operacion = tipo_operacion
        # CODIGO DE AYUDA REFERENCIA PARA LA EJECUCION
        # self.resultado_valor_izq = None
        # self.resultado_valor_der = None
        # self.last_scope = None

    def __str__(self):
        return f"Aritmetica -> Tipo: {self.tipo}"

    def verificarTipos(self, val_izquierdo, val_derecho):

        if (val_izquierdo == None or val_derecho == None):
            return False

        # extraemos el tipo de la exprecion izquierda de la op
        tipo_exprecion_izquierda = val_izquierdo["tipo"]
        # extraemos el tipo de la exprecion derecha de la op
        tipo_exprecion_der = val_derecho["tipo"]

        # print('debuj val izquierdo -> ',val_izquierdo)
        # print('debuj val derecho -> ',val_derecho)

        # extraemos el tipo de operacion que se quiere realizar
        tipo_operacion = self.tipo_operacion

        if (tipo_operacion == "+"):
            # si se trata de una suma enviamos a validarla
            return self.validar_suma(tipo_exprecion_izquierda, tipo_exprecion_der)
        else:
            return self.validar_otrasOperaciones(tipo_exprecion_izquierda, tipo_exprecion_der)

    def validar_suma(self, tipo_exprecion_izquierda, tipo_exprecion_der):
        # si se trata de una suma debemos verificar que los dos tipos sean iguales y sean string o number
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER or tipo_exprecion_izquierda == TipoEnum.STRING)):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            self.resultado.add_error(
                'Semantico', f'Tipos no coinciden para la operacion {self.tipo_operacion} , Se esperaba number {self.tipo_operacion} number | string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}', self.linea, self.columna)
            return False

    def validar_otrasOperaciones(self, tipo_exprecion_izquierda, tipo_exprecion_der):
        # si se trata de una operacion que no es una suma debemos verificar que los dos tipos sean iguales y number
        if (tipo_exprecion_izquierda == tipo_exprecion_der and (tipo_exprecion_izquierda == TipoEnum.NUMBER)):
            # si la verificacion se cumple entonces pasamos del metodo
            return True
        else:
            concat = f'Tipos no coinciden para la operacion {self.tipo_operacion}, Se esperaba number {self.tipo_operacion} number o string {self.tipo_operacion} string y se recibio {tipo_exprecion_izquierda.value} {self.tipo_operacion} {tipo_exprecion_der.value}'
            self.resultado.add_error(
                'Semantico', concat, self.linea, self.columna)

            return False

    def ejecutar(self, scope):

        val_izquierdo = self.expresion_izquierda.ejecutar(scope)
        val_derecho = self.expresion_derecha.ejecutar(scope)

        self.resultado_valor_izq = val_izquierdo
        self.resultado_valor_der = val_derecho
        self.last_scope = scope
        # print('Debuj-> Aritmetica -> tipo_operacion: ',self.tipo_operacion)
        # print('Debuj-> Aritmetica -> Izquierdo: ',val_izquierdo)
        # print('Debuj-> Aritmetica -> Derecho: ',val_derecho)

        if (self.verificarTipos(val_izquierdo, val_derecho)):
            result = None
            if (self.tipo_operacion == "+"):
                return {"value": result, "tipo": val_izquierdo['tipo'], "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "-"):
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "*"):
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "/"):
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "%"):
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            elif (self.tipo_operacion == "^"):
                return {"value": result, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            # print('Debuj-> Primitivo ->', self)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.tipo_operacion, padre)
        self.expresion_izquierda.graficar(graphviz, result)
        self.expresion_izquierda.graficar(graphviz, result)

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        temporal = ''
        operador = ''

        # Recuperamos los valores
        val_izq: Return = None
        val_der: Return = None
        val_izq: Return = self.expresion_izquierda.generar_c3d(scope)
        if isinstance(val_izq, Excepcion):
            return val_izq
        if isinstance(self.expresion_derecha, ValFuncion):
            self.expresion_derecha.guardar_temporales(generador, scope, [val_izq.get_value()])
            val_der: Return = self.expresion_derecha.generar_c3d(scope)
            if isinstance(val_der, Excepcion):
                return val_der
            self.expresion_derecha.recuperar_temporales(generador, scope, [val_izq.get_value()])
        else:
            val_der: Return = self.expresion_derecha.generar_c3d(scope)
            if isinstance(val_der, Excepcion):
                return val_der

        if val_izq.get_tipo() != val_der.get_tipo():
            print('Error en aritmetica')

        if (self.tipo_operacion == "+"):
            if val_izq.get_tipo() == TipoEnum.NUMBER:
                operador = '+'
                temporal = generador.add_temp()
                generador.add_exp(temporal, val_izq.get_value(),
                                  val_der.get_value(), operador)
                return Return(temporal, TipoEnum.NUMBER, True, None)
            elif val_izq.get_tipo() == TipoEnum.STRING:
                self.tipo = TipoEnum.STRING
                return self.suma_de_strings(val_izq.get_value(), val_der.get_value(), scope, generador)
            else:
                print('Fallo de calculo de tipo')
        elif (self.tipo_operacion == "-"):
            operador = '-'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),
                              val_der.get_value(), operador)
            return Return(temporal, TipoEnum.NUMBER, True, None)
        elif (self.tipo_operacion == "*"):
            operador = '*'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),
                              val_der.get_value(), operador)
            return Return(temporal, TipoEnum.NUMBER, True, None)
        elif (self.tipo_operacion == "/"):
            operador = '/'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),
                              val_der.get_value(), operador)
            return Return(temporal, TipoEnum.NUMBER, True, None)
        elif (self.tipo_operacion == "%"):
            operador = '%'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),
                              val_der.get_value(), operador)
            return Return(temporal, TipoEnum.NUMBER, True, None)
        elif (self.tipo_operacion == "^"):
            operador = '^'
            temporal = generador.add_temp()
            generador.add_exp(temporal, val_izq.get_value(),
                              val_der.get_value(), operador)
            return Return(temporal, TipoEnum.NUMBER, True, None)

    def suma_de_strings(self, valor_izquierda, valor_derecha, scope, generador: Generador):

        # envihamos ha generar la funcion de sumas
        generador.sum_strings()
        # generamos el primer temporal
        param_temp = generador.add_temp()
        generador.add_exp(param_temp, 'P', scope.size, '+')
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, valor_izquierda)

        # asignamos el segundo valor a la posicion 3 del stack
        generador.add_exp(param_temp, param_temp, '1', '+')
        generador.set_stack(param_temp, valor_derecha)

        # generar un nuevo entorno
        generador.new_env(scope.size)
        # llamamos a la funcion de sumar strings
        generador.call_fun("sumStrings")

        # anadir un nuevo temporal que guardara el stack en P
        temp = generador.add_temp()
        generador.get_stack(temp, 'P')
        # retornamos el un entorno
        generador.ret_env(scope.size)

        generador.add_comment('Fin de la suma de strings')
        generador.add_space()

        result = Return(temp, TipoEnum.STRING, False, None)

        return result
