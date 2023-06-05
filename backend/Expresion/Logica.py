from enum import Enum
from Abstracto.Exprecion import Expresion
from Abstracto.Tipo import TipoEnum
from Abstracto.Tipo import Tipo
from Abstracto.Retorno import Retorno


class OpcionLogica(Enum):
    AND = 0
    OR = 1
    NOT = 2


class Logica(Expresion):
    def __init__(self, linea, columna, izquierda: Expresion, derecha: Expresion, tipo: OpcionLogica):
        super().__init__(linea, columna)
        self.valOperacion = ['&&', '||', '!']
        self.izquierda = izquierda
        self.derecha = derecha
        self.tipo = tipo

    def ejecutar(self, scope) -> Retorno:
        valor_izquierdo = self.izquierda.ejecutar(scope)
        valor_derecha = self.derecha.ejecutar(scope)

        if (self.tipo == OpcionLogica.NOT):
            if (valor_derecha.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado derecho ,Linea: "+self.linea+" ,Columna: "+self.columna)
        else:

            if (valor_izquierdo.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado izquierdo ,Linea: "+self.linea+" ,Columna: "+self.columna)

            if (valor_derecha.tipo.get_tipo() != TipoEnum.BOOLEAN):
                raise ValueError(
                    "Para realizar una operacion logica se necesita de un valor booleano al lado derecho ,Linea: "+self.linea+" ,Columna: "+self.columna)

        result = None

        if (self.tip == OpcionLogica.AND):
            result = valor_izquierdo and valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))
        elif (self.tip == OpcionLogica.OR):
            result = valor_izquierdo or valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))
        elif (self.tip == OpcionLogica.NOT):
            result = not valor_derecha
            return Retorno(result, Tipo(TipoEnum.BOOLEAN, None))

        return Retorno(None, Tipo(TipoEnum.ERROR, None))



    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            '[label="' + self.valOperacion[self.tipo] + '",shape="circle"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)

        self.izquierda.graficar(scope, graphviz, ("nodo" + num))
        self.derecha.graficar(scope, graphviz, ("nodo" + num))
