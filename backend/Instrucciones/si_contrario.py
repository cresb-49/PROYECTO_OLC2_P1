from Abstract.abstract import Abstract
from Symbol.scope import Scope


class SiContrario(Abstract):

    def __init__(self, resultado, linea, columna, exprecion_condicion, codigo_true, codigo_false):
        super().__init__(resultado, linea, columna)
        self.exprecion_condicion = exprecion_condicion
        self.sentencias_true = codigo_true
        self.sentencias_false = codigo_false

    def __str__(self):
        return f"SiContrario: resultado={self.resultado}, linea={self.linea}, columna={self.columna}, exprecion_condicion={self.exprecion_condicion}, sentencias_true={self.sentencias_true}, sentencias_false={self.sentencias_false}"

    def ejecutar(self, scope):
        condicion = self.exprecion_condicion.ejecutar(scope)
        if condicion:
            new_scope = Scope(scope)
            return self.sentencias_true.ejecutar(new_scope)
        else:
            new_scope = Scope(scope)
            return self.sentencias_false.ejecutar(new_scope)

    def graficar(self, scope, graphviz, subNameNode, padre):
        pass
