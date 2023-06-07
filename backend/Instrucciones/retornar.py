from Abstract.abstract import Abstract


class Retornar(Abstract):
    def __init__(self, linea, columna, exprecion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def __str__(self):
        return f"Return -> Expresión: {self.exprecion}"

    def ejecutar(self, scope):
        valor = self.exprecion.ejecutar(scope)
        return valor
