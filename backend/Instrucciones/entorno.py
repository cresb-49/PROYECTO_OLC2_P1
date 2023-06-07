from Abstract.abstract import Abstract
from Instrucciones.funcion import Funcion


class Entorno(Abstract):
    def __init__(self, linea, columna, scope_global, intrucciones: list):
        super().__init__(linea, columna)
        self.scope_global = scope_global
        self.sentencias = intrucciones

    def __str__(self) -> str:
        return super().__str__()

    def ejecutar(self, scope):
        for instr in self.intrucciones:
            if isinstance(instr, Funcion):
                pass
            else:
                instr.ejecutar(self.scope_global)
