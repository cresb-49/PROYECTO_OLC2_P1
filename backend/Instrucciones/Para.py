from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum

class Para(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)
        
    def ejecutar(self, scope) -> any:
        print(scope)
        return None