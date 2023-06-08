from Abstract.abstract import Abstract
from Symbol.scope import Scope

class Contrario(Abstract):

    def __init__(self, resultado, linea, columna, sentencias):
        super().__init__(resultado, linea, columna)
        self.sentencias = sentencias

    def __str__(self):
        return f"Contrario: resultado={self.resultado}, linea={self.linea}, columna={self.columna}, sentencias={self.sentencias}"
    
    def ejecutar(self,scope):
        try:
            if self.sentencias != None:
                new_scope = Scope(scope)
                return self.sentencias.ejecutar(new_scope)
        except Exception:
            print('No se puede operar la sentencia existe un error anterior')
    
    def graficar(self, scope, graphviz, subNameNode, padre):
        pass