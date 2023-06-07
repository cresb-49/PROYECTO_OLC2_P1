from Abstract.abstract import Abstract


class Si(Abstract):
    def __init__(self, linea, columna, exprecion, sentencias, _else):
        super().__init__(linea, columna)
        self.exprecion = exprecion
        self.sentencias = sentencias
        self._else = _else

    def __str__(self):
        return f"If -> Expresión: {self.exprecion}, Sentencias: {self.sentencias}, Else: {self._else}"

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        if result:
            self.sentencias.ejecutar(scope)
        else:
            self._else.ejecutar(scope)
