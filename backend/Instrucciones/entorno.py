from Abstract.abstract import Abstract

class Entorno(Abstract):
    def __init__(self, resultado,linea, columna, scope_global, intrucciones):
        super().__init__(resultado,linea, columna)
        self.scope_global = scope_global
        self.intrucciones = intrucciones

    def __str__(self) -> str:
        return super().__str__()

    def ejecutar(self, scope):
        self.intrucciones.ejecutar(self.scope_global)

    #Grafica un entorono enviando instricciones a graphviz, debera implementarse
    def graficar(self, scope, graphviz, subNameNode, padre):
        pass
