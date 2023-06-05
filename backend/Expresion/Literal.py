from Abstracto.Exprecion import Expresion
from Abstracto.Retorno import Retorno
from Abstracto.Tipo import Tipo


class Literal(Expresion):
    def __init__(self, linea, columna, valor, tipo: Tipo):
        super().__init__(linea, columna)
        self.valor = valor
        self.tipo = tipo

    def ejecutar(self, scope) -> Retorno:
        return Retorno(self.valor, self.tipo)

    def graficar(self, scope, graphviz, padre):
        num = graphviz.declaraciones.length + 1
        node = "nodo" + num + \
            ' [label="<f0> ' + Tipo.get_tipo_string() + \
            ' |<f1> ' + self.valor + '"];'
        graphviz.declaraciones.push(node)
        if (padre.length != 0):
            relacion = padre + ' -> ' + "nodo" + num
            graphviz.relaciones.push(relacion)
