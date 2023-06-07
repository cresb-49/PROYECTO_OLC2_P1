from Abstract.abstract import Abstract


class Detener(Abstract):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def __str__(self):
        return "Break"
    
    def ejecutar(self, scope) -> any:
        return None
