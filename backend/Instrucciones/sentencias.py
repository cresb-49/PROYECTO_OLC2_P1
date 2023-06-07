from Abstract.abstract import Abstract
from Symbol.scope import Scope

from Instrucciones.continuar import Continuar
from Instrucciones.detener import Detener
from Instrucciones.retornar import Retornar

class Sentencias(Abstract):
    def __init__(self, linea, columna, intrucciones:list):
        super().__init__(linea, columna)
        self.intrucciones = intrucciones

    def ejecutar(self, scope):
        scope:Scope = Scope(scope)
        for instr in self.intrucciones:
            print(instr)
