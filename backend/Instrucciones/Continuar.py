from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope


class Continuar(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def ejecutar(self, scope: Scope) -> any:
        return None
