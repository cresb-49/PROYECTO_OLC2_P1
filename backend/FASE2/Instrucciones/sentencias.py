from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.scope import Scope

from FASE2.Instrucciones.funcion import Funcion
from FASE2.Instrucciones.continuar import Continuar
from FASE2.Instrucciones.detener import Detener
from FASE2.Instrucciones.retornar import Retornar


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
                result = self.intr_izquierda.ejecutar(scope)
                if isinstance(result, dict) or isinstance(result, Continuar) or isinstance(result, Detener):
                    # TODO: [IMPORTANTE] Eliminar debuj
                    #print('debuj sentencias:', result)
                    return result

        if self.instr_derecha != None:
            if not (isinstance(self.instr_derecha, Funcion)):
                result = self.instr_derecha.ejecutar(scope)
                if isinstance(result, dict) or isinstance(result, Continuar) or isinstance(result, Detener):
                    # TODO: [IMPORTANTE] Eliminar debuj
                    #print('debuj sentencias:', result)
                    return result

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('instr', padre)
        if self.intr_izquierda != None:
            self.intr_izquierda.graficar(graphviz, result)
        if self.instr_derecha != None:
            self.instr_derecha.graficar(graphviz, result)

    def generar_c3d(self,scope):
        if self.intr_izquierda != None:
            result = self.intr_izquierda.generar_c3d(scope)
            if isinstance(result, Return):
                return result
        if self.instr_derecha != None:
            result = self.instr_derecha.generar_c3d(scope)
            if isinstance(result, Return):
                return result