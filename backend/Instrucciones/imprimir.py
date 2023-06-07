from Abstract.abstract import Abstract


class Imprimir(Abstract):
    def __init__(self, linea, columna, exprecion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def ejecutar(self, scope) -> any:
        resultado = self.exprecion.ejecutar(scope)
        print(resultado)
        return None
