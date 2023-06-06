from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Abstracto.Retorno import Retorno
from Simbolo.Scope import Scope

from Detener import Detener
from Continuar import Continuar
from Retornar import Retornar
from Exprecion.Literal import Literal


class Sentencias(Instruccion):
    def __init__(self, linea, columna, intrucciones: list):
        super().__init__(linea, columna)
        self.intrucciones = Instruccion

    def ejecutar(self, scope: Scope) -> Retorno:

        for instr in self.intrucciones:
            if isinstance(instr, Instruccion):
                if isinstance(instr, Detener):
                    return instr
                elif isinstance(instr, Continuar):
                    return instr
                elif isinstance(instr, Retornar):
                    elemento = instr.ejecutar(scope)
                    return Retornar(Literal(elemento.value, instr.linea, instr.columna, elemento.tipo), instr.linea, instr.columna)
                else:
                    elemento = instr.ejecutar(scope)
                    if isinstance(elemento, Detener):
                        return elemento
                    elif isinstance(elemento, Continuar):
                        return elemento
                    elif isinstance(elemento, Retornar):
                        ele = elemento.ejecutar(scope)
                        return Retornar(Literal(ele.value, instr.linea, instr.columna, ele.tipo), instr.linea, instr.columna)


    def graficar(self, scope, graphviz, subNameNode, padre):
        #iteramos en cada una de las instrucciones de la lista y ejecutamos su metodo graficar
        for intructions in self.intrucciones:
            intructions.graficar(scope, graphviz, subNameNode, padre)
