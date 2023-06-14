from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum
from Expresiones.arreglo import Arreglo


class Declaracion(Abstract):
    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, valor):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.tipo_secundario = tipo_secundario

    def __str__(self):
        return f"Declaracion: {self.id}, Tipo: {self.tipo}, Valor: {self.valor}"

    def ejecutar(self, scope):
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
        if len(resultado) == 0:
            return {"value": [], "tipo": TipoEnum.ARRAY, "tipo_secundario": tipo_variable_contenedora, "linea": self.linea, "columna": self.columna}
        else:
            base = resultado[0]['tipo']
            if all(base == exp['tipo'] for exp in resultado):
                return {"value": resultado, "tipo": TipoEnum.ARRAY, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": resultado, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        node_result = graphviz.add_nodo("Declaracion", padre)
        graphviz.add_nodo(self.id, node_result)
        igual = graphviz.add_nodo('=', node_result)
        if (self.valor != None):
            self.valor.graficar(graphviz, igual)
