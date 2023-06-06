from Abstracto.Instruccion import Instruccion
from Abstracto.Exprecion import Exprecion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope


class Retornar(Instruccion):
    def __init__(self, linea, columna, exprecion: Exprecion):
        super().__init__(linea, columna)
        self.exprecion = exprecion

    def ejecutar(self, scope: Scope) -> any:
        valor = self.exprecion.ejecutar(scope)
        return valor

    def graficar(scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Retorno"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        nume2 = graphviz.declaraciones.length + 1
        node2 = "nodo_" + subNameNode + "_" + nume2
        decl2 = node2 + '[label = "<n>Exprecion"];'
        graphviz.declaraciones.push(decl2)
        graphviz.relaciones.push((node + ':n -> ' + node2 + ':n'))
