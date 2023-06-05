from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Abstracto.Exprecion import Expresion
from Simbolo.Scope import Scope


class Asignacion(Instruccion):
    def __init__(self, linea, columna, identificador: str, valor: Expresion):
        super().__init__(linea, columna)
        self.id= identificador
        self.valor = valor

    def ejecutar(self, scope: Scope) -> any:
        result = self.valor.ejecutar(scope)
        scope.modificar_variable(self.id,result.value,result.tipo)
        
