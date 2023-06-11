from Abstract.abstract import Abstract
from Symbol.scope import Scope

from Instrucciones.funcion import Funcion
from Instrucciones.continuar import Continuar
from Instrucciones.detener import Detener
from Instrucciones.retornar import Retornar


class Sentencias(Abstract):
    def __init__(self, resultado, linea, columna, intr_izquierda, instr_derecha):
        super().__init__(resultado, linea, columna)
        self.intr_izquierda = intr_izquierda
        self.instr_derecha = instr_derecha

    def __str__(self):
        return f"instr: izquierda: {str(self.intr_izquierda)}, derecha: {str(self.instr_derecha)}"

    def ejecutar(self, scope):
        # Verificamos que la instruccion no sea una funcion para no ejecutarla
        if self.intr_izquierda != None:
            if not (isinstance(self.intr_izquierda, Funcion)):
                return self.intr_izquierda.ejecutar(scope)
        if self.instr_derecha != None:
            if not (isinstance(self.instr_derecha, Funcion)):
                return self.instr_derecha.ejecutar(scope)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('instruccion', padre)
        if self.intr_izquierda != None:
            self.intr_izquierda.graficar(graphviz, result)
        if self.instr_derecha != None:
            self.instr_derecha.graficar(graphviz, result)
