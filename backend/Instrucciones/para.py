from Abstract.abstract import Abstract

"""
tipo_for = 1 -> for (let i = 0; i < 10; i++) , declaracion, condicion, exprecion
tipo_for = 2 -> for (let var of var) , declaracion, exprecion
"""
class Para(Abstract):
    def __init__(self, linea, columna, tipo_for, declaracion, condicion, expresion):
        super().__init__(linea, columna)
        self.tipo_for = tipo_for
        self.declaracion = declaracion
        self.condicion = condicion
        self.expresion = expresion

    def ejecutar(self):
        if self.tipo_for == 1:
            print('Ejecutamos for tipo 1')
        else:
            print('Ejecutamos for tipo 2')
