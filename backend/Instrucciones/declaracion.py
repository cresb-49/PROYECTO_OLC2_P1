from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Declaracion(Abstract):
    def __init__(self, linea, columna, id, tipo, tipo_secundario, valor):
        super().__init__(linea, columna)
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
            scope.declarar_variable(
                self.id, result_expresion['value'], self.tipo, tipo_secundario.value, self.linea, self.columna)
        elif self.tipo == TipoEnum.ARRAY:
            if len(self.valor.arreglo) == len(result_expresion['value']):
                scope.declarar_variable(self.id, result_expresion, self.tipo, self.tipo_secundario, self.linea, self.columna)
            else:
                print('No se declaro el array', self.linea, self.columna)
        else:
            tipo: TipoEnum = result_expresion['tipo']
            scope.declarar_variable(
                self.id, result_expresion['value'], tipo, None, self.linea, self.columna)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Declaracion"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
