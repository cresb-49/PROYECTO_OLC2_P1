from Abstract.abstract import Abstract


class Detener(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope) -> any:
        return None
