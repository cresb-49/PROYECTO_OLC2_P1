from Abstracto.Instruccion import Instruccion
from Abstracto.Exprecion import Expresion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope


class Retornar(Instruccion):
    def __init__(self, linea, columna, exprecion: Expresion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def ejecutar(self, scope: Scope) -> any:
        valor = self.exprecion.ejecutar(scope)
        return valor
