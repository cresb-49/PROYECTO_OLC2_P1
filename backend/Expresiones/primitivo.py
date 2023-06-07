from Abstract.abstract import Abstract

class Primitivo(Abstract):
    def __init__(self, linea, columna,tipo,valor):
        super().__init__(linea, columna)
        self.tipo = tipo
        self.valor = valor
    
    def ejecutar(self, scope):
        return self.valor