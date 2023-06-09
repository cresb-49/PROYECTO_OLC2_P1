from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class ToString(Abstract):

    def __init__(self, resultado, linea, columna, numero):
        super().__init__(resultado, linea, columna)
        self.numero = numero

    def __str__(self):
        return "Concat"

    def ejecutar(self, scope):
        # ejecutamos el diccionario
        ejecutar = self.numero.ejecutar(scope)
        # mandmaos ha hacer concat sobre el atributo value
        toString = FuncionNativa.hacer_to_string(None, ejecutar['value'])
        #retornamos un diccionario con la String realizada y el tipo String
        return {"value": toString, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Concat"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
