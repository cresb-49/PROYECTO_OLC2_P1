from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope
from enum import Enum
from Exprecion.Operacion import OpcionOperacion
from Exprecion.Acceder import Acceder
from Exprecion.Literal import Literal
from Exprecion.Operacion import Operacion
from Asignacion import Asignacion
from Detener import Detener
from Continuar import Continuar
from Retornar import Retornar
from Sentencias import Sentencias
from Abstracto.Exprecion import Exprecion

class OpcionPara(Enum):
    SUM_PARA = 0
    RES_PARA = 1


class Para(Instruccion):
    def __init__(self, linea, columna, opPara:int, valVar: Exprecion, varIterator:str, sentencias: Sentencias, expr:Exprecion):
        super().__init__(linea, columna)
        self.opPara = opPara
        self.valVar = valVar
        self.varIterator = varIterator
        self.sentencias = sentencias
        self.expr = expr

    def ejecutar(self, scope: Scope) -> any:
        newScope = Scope
        paso = 0
        if (self.opPara == OpcionPara.SUM_PARA):
            paso = 1
        else:
            paso = -1

        exp1 = Acceder(self.varIterator, self.linea, self.columna)
        exp2 = Literal(paso, self.linea, self.columna, Tipo.INT)

        value = self.valVar.ejecutar(newScope)
        newScope.declararVariable(
            self.varIterator, value.value, Tipo.INT, self.linea, self.columna)

        newVal = Operacion(exp1, exp2, OpcionOperacion.SUMA,
                           self.linea, self.columna)
        asignar = Asignacion(self.varIterator, newVal,
                             self.linea, self.columna)

        condicion = self.expr.ejecutar(newScope)

        if (condicion.tipo != Tipo.BOOLEAN):
            raise ValueError(
                "La condicion de Para no es Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

        while (condicion.value):
            result = self.sentencias.ejecutarPara(newScope)
            if (isinstance(Detener, result)):
                break
            elif (isinstance(Continuar, result)):
                asignar.ejecutar(newScope)
                condicion = self.expr.ejecutar(newScope)
                continue
            elif (isinstance(Retornar, result)):
                return result

            asignar.ejecutar(newScope)
            condicion = self.expr.ejecutar(newScope)
            if (condicion.tipo != Tipo.BOOLEAN):
                raise ValueError(
                    "La condicion de Para no es Boolean Linea: "+self.linea+" ,Columna: "+self.columna)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Para"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        self.sentencias.graficar(scope, graphviz, subNameNode, node)
