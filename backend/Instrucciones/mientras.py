from Abstract.abstract import Abstract


class Mientras(Abstract):
    def __init__(self, linea, columna, condicion, sentencias):
        super().__init__(linea, columna)
        self.condicion = condicion
        self.sentencias = sentencias

    def ejecutar(self, scope):
        condicion = self.condicion.ejecutar(scope)
