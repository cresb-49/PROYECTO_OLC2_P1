from Abstract.abstract import Abstract


class IntruccionError(Abstract):
    def __init__(self, resultado, linea, columna):
        super().__init__(resultado, linea, columna)

    def __str__(self):
        return f"IntruccionError: Línea: {self.linea}, Columna: {self.columna}"

    def ejecutar(self, scope):
        print(self)

    def graficar(self, graphviz, padre):
        pass
