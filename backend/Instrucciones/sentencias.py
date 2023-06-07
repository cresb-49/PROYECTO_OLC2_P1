from Abstract.abstract import Abstract
from Symbol.scope import Scope

from Instrucciones.continuar import Continuar
from Instrucciones.detener import Detener
from Instrucciones.retornar import Retornar


class Sentencias(Abstract):
    def __init__(self, linea, columna, intr_izquierda, instr_derecha):
        super().__init__(linea, columna)
        self.intr_izquierda = intr_izquierda
        self.instr_derecha = instr_derecha

    def __str__(self):
        return f"instr: izquierda: {str(self.intr_izquierda)}, derecha: {str(self.instr_derecha)}"

    def ejecutar(self, scope):
        if self.intr_izquierda != None:
            self.intr_izquierda.ejecutar(scope)
        if self.instr_derecha != None:
            self.instr_derecha.ejecutar(scope)
