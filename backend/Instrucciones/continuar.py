from Abstract.abstract import Abstract


class Continuar(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def __str__(self):
        return "Continuar"

    def ejecutar(self, scope):
        return None
