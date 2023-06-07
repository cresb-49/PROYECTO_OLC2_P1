from Abstract.abstract import Abstract
from Instrucciones.funcion import Funcion


class Entorno(Abstract):
    def __init__(self, linea, columna, scope_global, intrucciones):
        super().__init__(linea, columna)
        self.scope_global = scope_global
        self.intrucciones = intrucciones

    def __str__(self) -> str:
        return super().__str__()

    def ejecutar(self, scope):
        self.intrucciones.ejecutar(self.scope_global)
