from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


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
            try:
                scope.declarar_variable(self.id, result_expresion['value'], self.tipo, tipo_secundario.value, self.linea, self.columna)
            except ValueError as error:
                self.resultado.add_error('Semantico',str(error),self.linea,self.columna)
                print('Semantico',str(error),self.linea,self.columna)
        elif self.tipo == TipoEnum.ARRAY:
            if len(self.valor.arreglo) == len(result_expresion['value']):
                try:
                    scope.declarar_variable(
                        self.id, result_expresion['value'], self.tipo, self.tipo_secundario, self.linea, self.columna)
                except ValueError as error:
                    self.resultado.add_error('Semantico',str(error),self.linea,self.columna)
                    print('Semantico',str(error),self.linea,self.columna)
            else:
                self.resultado.add_error(
                    'Semantico', 'No se declaro el array', self.linea, self.columna)
        else:
            tipo: TipoEnum = result_expresion['tipo']
            #TODO: Verificar por si hay errores mas adelante en la asignacion
            if self.tipo == result_expresion['tipo'] or self.tipo == None:
                try:
                    scope.declarar_variable(
                        self.id, result_expresion['value'], tipo, None, self.linea, self.columna)
                except ValueError as error:
                    self.resultado.add_error('Semantico',str(error),self.linea,self.columna)
                    print('Semantico',str(error),self.linea,self.columna)
            else:
                error = f'No se pude declarar la variable "{self.id}" de tipo : {tipo.value} y asignar un valor tipo: {tipo.value}'
                self.resultado.add_error('Semantico', error, self.linea, self.columna)

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        igual = graphviz.add_nodo('=', padre)
        if (self.valor != None):
            self.valor.graficar(graphviz, igual)
