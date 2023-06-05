from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Simbolo.Scope import Scope
from Sentencias import Sentencias
from Abstracto.Retorno import Retorno


class Funcion(Instruccion):

    def __init__(self, linea, columna, identificador: str, tipo: Tipo, sentancias: Sentencias | None):
        super().__init__(linea, columna)
        self.id = identificador
        self.tipo = tipo
        self.sentencias = sentancias

    def ejecutar(self, scope: Scope) -> Retorno:
        result = self.sentencias.ejecutar(scope)
        return result

    def graficar(self, scope, graphviz, padre) -> None:
        print("Graficacion de una funcion")
