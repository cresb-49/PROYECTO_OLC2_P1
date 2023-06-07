from Abstract.abstract import Abstract


class Continuar(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope):
        return None
