from Abstract.abstract import Abstract
from Symbol.scope import Scope

class Sentencias(Abstract):
    def __init__(self, linea, columna, intrucciones:list):
        super().__init__(linea, columna)
        self.intrucciones = intrucciones

    def ejecutar(self, scope):
        scope = Scope(scope)
        for instr in self.intrucciones:
            print(instr)
