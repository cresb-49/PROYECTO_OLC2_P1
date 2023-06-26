from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope
from FASE2.Expresiones.arreglo import Arreglo
from FASE2.Symbol.Exception import Excepcion


class Declaracion(Abstract):
    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, valor):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.tipo_secundario = tipo_secundario
        # CODIGO DE AYUDA REFERENCIA PARA LA EJECUCION
        self.resultado_valor = None
        self.last_scope = None
        self.find = True
        self.ghost = -1

    def __str__(self):
        return f"Declaracion: {self.id}, Tipo: {self.tipo}, Valor: {self.valor}"

    def ejecutar(self, scope):
        # Guardado del scope de trabajo
        self.last_scope = scope
        result_expresion = None
        if (self.valor != None):
            result_expresion = self.valor.ejecutar(scope)
        else:
            if self.tipo == TipoEnum.ANY:
                result_expresion = {"value": '', "tipo": TipoEnum.STRING,
                                    "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                result_expresion = {"value": None, "tipo": self.tipo,
                                    "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        # Asignacion del resultado obtenido en esta intruccion
        self.resultado_valor = result_expresion
        if self.tipo == TipoEnum.ANY:
            tipo_secundario: TipoEnum = result_expresion['tipo']
            # print(f'Declaro variable "{self.id}" con ->',result_expresion)
            try:
                scope.declarar_variable(
                    self.id, result_expresion['value'], self.tipo, tipo_secundario.value, self.linea, self.columna)

            except ValueError as error:
                self.resultado.add_error('Semantico', str(
                    error), self.linea, self.columna)
                print('Semantico', str(error), self.linea, self.columna)
        elif self.tipo == TipoEnum.ARRAY:
            # Resolvemos el array y verificamos que este completo como al inicio
            # if isinstance(self.valor, Arreglo):
            if isinstance(result_expresion, Arreglo):
                if len(self.valor.arreglo) == len(result_expresion['value']):
                    if self.tipo_secundario == result_expresion['tipo_secundario']:
                        try:
                            scope.declarar_variable(
                                self.id, result_expresion['value'], self.tipo, self.tipo_secundario, self.linea, self.columna)

                        except ValueError as error:
                            self.resultado.add_error('Semantico', str(
                                error), self.linea, self.columna)
                            print('Semantico', str(error),
                                  self.linea, self.columna)
                    else:
                        self.resultado.add_error(
                            'Semantico', f'Al crear un array de tipo: {self.tipo_secundario} debe de asignar un array del mismo tipo, esta asignano uno de tipo: {result_expresion["tipo_secundario"]}', self.linea, self.columna)
                else:
                    self.resultado.add_error(
                        'Semantico', 'Hay errores previos antes de la declracion del array', self.linea, self.columna)
            else:
                if result_expresion['tipo'] == TipoEnum.ARRAY:
                    # Validacion de tipos secundarios
                    if result_expresion['tipo_secundario'] == None:
                        # Calculo del tipo secundario debido a que viene de un any

                        arreglo = self.calculo_tipo_array(
                            result_expresion['value'], self.tipo_secundario)
                        if arreglo['tipo_secundario'] == self.tipo_secundario:
                            scope.declarar_variable(
                                self.id, result_expresion['value'], self.tipo, self.tipo_secundario, self.linea, self.columna)

                        else:
                            error = f'No puede declarar un varaible array de tipo: {self.tipo_secundario} y asignar un tipo: ' + str(
                                arreglo['tipo_secundario'])
                            self.resultado.add_error(
                                'Semantico', error, self.linea, self.columna)
                            print('Semantico', str(error),
                                  self.linea, self.columna)

                    elif result_expresion['tipo_secundario'] == self.tipo_secundario or self.tipo_secundario == TipoEnum.ANY.value:

                        scope.declarar_variable(
                            self.id, result_expresion['value'], self.tipo, self.tipo_secundario, self.linea, self.columna)

                    else:

                        error = f'No puede declarar un varaible array de tipo: {self.tipo_secundario} y asignar un tipo: ' + str(
                            result_expresion['tipo_secundario'])
                        self.resultado.add_error(
                            'Semantico', error, self.linea, self.columna)
                        print('Semantico', str(error),
                              self.linea, self.columna)
                else:
                    error = 'No puede declarar un varaible array y asignar un tipo: ' + \
                        str(result_expresion['tipo'])
                    self.resultado.add_error(
                        'Semantico', error, self.linea, self.columna)
                    print('Semantico', str(error), self.linea, self.columna)
        elif self.tipo == TipoEnum.STRUCT:
            if self.tipo == result_expresion['tipo']:
                if result_expresion['tipo_secundario'] == self.tipo_secundario:
                    try:
                        scope.declarar_variable(
                            self.id, result_expresion['value'], result_expresion['tipo'], result_expresion['tipo_secundario'], self.linea, self.columna)

                    except ValueError as error:
                        self.resultado.add_error('Semantico', str(
                            error), self.linea, self.columna)
                        print('Semantico', str(error),
                              self.linea, self.columna)
                else:
                    error = f'No puede declarar un varaible struct tipo "{self.tipo_secundario}" y asignar un struct de tipo {result_expresion["tipo_secundario"]}'
                    self.resultado.add_error(
                        'Semantico', error, self.linea, self.columna)
            else:
                error = 'No puede declarar un varaible struct y asignar un tipo: ' + \
                    str(result_expresion['tipo'])
                self.resultado.add_error(
                    'Semantico', error, self.linea, self.columna)
        else:
            if (result_expresion != None):
                tipo: TipoEnum = result_expresion['tipo']
                # TODO: Verificar por si hay errores mas adelante en la asignacion
                if self.tipo == result_expresion['tipo'] or self.tipo == None:
                    try:
                        scope.declarar_variable(
                            self.id, result_expresion['value'], tipo, None, self.linea, self.columna)

                    except ValueError as error:
                        self.resultado.add_error('Semantico', str(
                            error), self.linea, self.columna)
                        print('Semantico', str(error),
                              self.linea, self.columna)
                else:
                    error = f'No se pude declarar la variable "{self.id}" de tipo : {tipo.value} y asignar un valor tipo: {tipo.value}'
                    self.resultado.add_error(
                        'Semantico', error, self.linea, self.columna)
                    print('Semantico', str(error), self.linea, self.columna)
            else:
                error = f'No se pude declarar la variable "{self.id}" no existe valor para asignar'
                self.resultado.add_error(
                    'Semantico', error, self.linea, self.columna)
                print('Semantico', str(error), self.linea, self.columna)

    def calculo_tipo_array(self, resultado, tipo_variable_contenedora):
        if resultado == None:
            return {"value": [], "tipo": TipoEnum.ARRAY, "tipo_secundario": tipo_variable_contenedora, "linea": self.linea, "columna": self.columna}
        elif len(resultado) == 0:
            return {"value": [], "tipo": TipoEnum.ARRAY, "tipo_secundario": tipo_variable_contenedora, "linea": self.linea, "columna": self.columna}
        else:
            base = resultado[0]['tipo']
            if all(base == exp['tipo'] for exp in resultado):
                return {"value": resultado, "tipo": TipoEnum.ARRAY, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": resultado, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        node_result = graphviz.add_nodo("declarar", padre)
        graphviz.add_nodo(self.id, node_result)
        if (self.valor != None):
            self.valor.graficar(graphviz, node_result)

    def validar_tipos(self, result: Return):
        if result == None:
            return True
        # print('debuj declaracion =>', self.tipo)
        if (result.get_tipo() == TipoEnum.ANY):
            if (self.tipo != result.get_tipo_aux() and self.tipo != TipoEnum.ANY):
                return False
            return True

        if (result.get_tipo() != self.tipo and self.tipo != TipoEnum.ANY):
            return False
        return True
        # if(self.tipo != result['tipo'] !=  TipoEnum.STRING):
        #     return False
        # if(self.tipo != result['tipo'] !=  TipoEnum.NUMBER):
        #     return False
        # if(self.tipo != result['tipo'] !=  TipoEnum.ARRAY):
        #     return False
        # if(self.tipo != result['tipo'] !=  TipoEnum.BOOLEAN):
        #     return False

    def validar_tipo_secundario(self, result: Return):
        if result == None:
            return True
        if self.tipo == TipoEnum.ANY:
            return True
        return self.get_enum() == result.get_tipo_aux()

    def get_enum(self):
        if self.tipo_secundario == TipoEnum.ANY.value:
            return TipoEnum.ANY
        elif self.tipo_secundario == TipoEnum.NUMBER.value:
            return TipoEnum.NUMBER
        elif self.tipo_secundario == TipoEnum.BOOLEAN.value:
            return TipoEnum.BOOLEAN
        elif self.tipo_secundario == TipoEnum.ARRAY.value:
            return TipoEnum.ARRAY
        elif self.tipo_secundario == TipoEnum.STRING.value:
            return TipoEnum.STRING
        elif self.tipo_secundario == TipoEnum.STRUCT.value:
            return TipoEnum.STRUCT
        else:
            return self.tipo_secundario

    def generar_c3d(self, scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        print('Verificacion en declaracion: ', self.tipo, self.tipo_secundario)
        # generamos el codigo 3 direccines de la asignacion si es que existe
        result: Return = None
        if self.valor != None:
            result = self.valor.generar_c3d(scope)
        # print('debuj declaracion',result)
        if (isinstance(result, Excepcion)):
            return result

        generador.add_comment(f'** compilacion de variable {self.id} **')

        if (self.validar_tipos(result)):
            if self.validar_tipo_secundario(result):
                self.declaracion(result, generador, scope)
            else:
                if self.tipo == TipoEnum.ARRAY:
                    error = f'No pude declrar un array de tipo {self.tipo_secundario} y asignarle un array de tipo {result.get_tipo_aux()}'
                    self.resultado.add_error(
                        'Semantico', error, self.linea, self.columna)
                    return Excepcion('Semantico', error, self.linea, self.columna)
                else:
                    error = f'No pude declrar un struct de tipo {self.tipo_secundario} y asignarle un struct de tipo {result.get_tipo_aux()}'
                    self.resultado.add_error(
                        'Semantico', error, self.linea, self.columna)
                    return Excepcion('Semantico', error, self.linea, self.columna)
        else:
           # si la vaidacion de tipos no se paso entonces agregamos un error de tipo semantico
            error = f'No se pude declarar la variable "{self.id}" puesto que es de tipo {self.tipo.value} y se le asigno {result.get_tipo().value}'
            # error = f'No se pude declarar la variable "{self.id}" puesto que es de tipo {self.tipo.value} y se le asigno'
            self.resultado.add_error(
                'Semantico', error, self.linea, self.columna)
            print('Semantico', str(error), self.linea, self.columna)
            return Excepcion("Semantico", error, self.linea, self.columna)

    def declaracion(self, result: Return, generador: Generador, scope: Scope):
        # Primero obtenermos la variable desde el scope generado por ultimo
        # Verificamos si el result es none ya que puede ser una declaracion vacia
        if result == None:
            scope.declarar_variable(self.id, None, self.tipo, self.tipo_secundario,
                                    self.tipo == TipoEnum.ANY, self.linea, self.columna)
        else:
            scope.declarar_variable(self.id, None, result.get_tipo(
            ), result.get_tipo_aux(), self.tipo == TipoEnum.ANY, self.linea, self.columna)
        # Codigo resultante
        variable_recuperada = scope.obtener_variable(self.id)
        # print('Variable -> ', variable_recuperada)
        tempPos = variable_recuperada.simbolo_c3d.pos
        temp_Pos = variable_recuperada.simbolo_c3d.pos
        if result != None:
            if result.get_tipo() == TipoEnum.ARRAY:
                variable_recuperada.simbolo_c3d.dimenciones = result.dimenciones

        if not variable_recuperada.simbolo_c3d.is_global:
            tempPos = generador.add_temp()
            generador.add_exp(tempPos, 'P', temp_Pos, '+')
        if result != None:
            if result.type == TipoEnum.BOOLEAN:
                temp_lbl = generador.new_label()
                for label in result.get_true_lbls():
                    generador.put_label(label)
                generador.set_stack(tempPos, "1")
                generador.add_goto(temp_lbl)
                for label in result.get_false_lbls():
                    generador.put_label(label)
                generador.set_stack(temp_Pos, "0")
                generador.put_label(temp_lbl)
            else:
                generador.set_stack(tempPos, result.value)
        else:
            generador.set_stack(tempPos, 0)
        generador.add_comment(f'** fin de compilacion variable {self.id} **')
        scope.sum_size()
        # print('last scope -> ', scope)
