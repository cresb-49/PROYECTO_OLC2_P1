from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope


class CallFuncion(Instruccion):
    def __init__(self, linea, columna, identificador: str, parametros: any):
        super().__init__(linea, columna)
        self.id = identificador
        self.parametros = parametros

    def ejecutar(self, scope: Scope) -> any:
        fun = scope.obtener_funcion(self.id)
        if(function != None):
            fun.ejecutar(scope)
        
        
