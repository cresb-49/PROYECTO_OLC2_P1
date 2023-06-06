from enum import Enum
from Abstracto.Exprecion import Exprecion
from Abstracto.Tipo import TipoEnum
from Abstracto.Tipo import Tipo
from Abstracto.Retorno import Retorno
from Simbolo.Scope import Scope

class ObtenerValFuncion(Exprecion):

    def __init__(self, linea, columna, identificador, parametros):
        super().__init__(linea, columna)
        self.identificador = identificador
        self.parametros = parametros

    def ejecutar(self, scope: Scope) -> Retorno:
        return Retorno(None,Tipo(TipoEnum.ERROR,None))

    def graficar(self, scope, graphviz, padre):
        print(scope, graphviz, padre)
        return None