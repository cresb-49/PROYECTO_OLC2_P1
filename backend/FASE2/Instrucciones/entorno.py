from FASE2.Abstract.abstract import Abstract


class Entorno(Abstract):
    def __init__(self, resultado, linea, columna, scope_global, intrucciones):
        super().__init__(resultado, linea, columna)
        self.scope_global = scope_global
        self.intrucciones = intrucciones

    def __str__(self) -> str:
        return super().__str__()

    def ejecutar(self, scope):
        codigo_referencia = str(id(self))
        # Registramos el entorno utilizado
        self.resultado.agregar_entorno(codigo_referencia, self.scope_global)
        self.intrucciones.ejecutar(self.scope_global)

    # Grafica un entorono enviando instricciones a graphviz, debera implementarse
    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('Inicio', padre)
        self.intrucciones.graficar(graphviz, result)

    def generar_c3d(self,scope):
        self.intrucciones.generar_c3d(self.scope_global)