from enum import Enum
from Abstracto.Exprecion import Exprecion
from Abstracto.Tipo import TipoEnum
from Abstracto.Tipo import Tipo
from Abstracto.Retorno import Retorno
from Simbolo.Scope import Scope

class OpcionRelacional(Enum):
    IGUAL = 0
    DIFERENTE = 1
    MENOR = 2
    MAYOR = 3
    MENOR_IGUAL = 4
    MAYOR_IGUAL = 5


class Relacional(Exprecion):
    def __init__(self, linea, columna, izquierda: Exprecion, derecha: Exprecion, tipo: OpcionRelacional):
        super().__init__(linea, columna)
        self.TipoRelacional = ['==', '!=', '<', '>', '<=', '>=']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope: Scope) -> Retorno:
        valor_izquierda = self.izquierda.ejecutar(scope)
        valor_derecha = self.derecha.ejecutar(scope)

        if (valor_izquierda.tipo.get_tipo() == Tipo.ERROR or valor_derecha.tipo.get_tipo() == Tipo.ERROR):
            raise ValueError("Errores previos antes de ralizar la comparacion , Linea: " +
                             self.linea + " ,Columna: " + self.columna)

        # Debemos de realizar la verificacion de los tipos de valores a comparar

        result = None

        if (self.tipo == OpcionRelacional.IGUAL):
            result = valor_izquierda == valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.DIFERENTE):
            result = valor_izquierda != valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MENOR):
            result = valor_izquierda < valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MAYOR):
            result = valor_izquierda > valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MENOR_IGUAL):
            result = valor_izquierda <= valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))
        elif (self.tipo == OpcionRelacional.MAYOR_IGUAL):
            result = valor_izquierda >= valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN))

        return Retorno(None, Tipo(TipoEnum.ERROR))

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + ' [label="' + self.TipoRelacional[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))
