from Abstract.abstract import Abstract
from Symbol.scope import Scope

"""
tipo_for = 1 -> for (let i = 0; i < 10; i++) , declaracion, condicion, exprecion
tipo_for = 2 -> for (let var of var) , declaracion, exprecion
"""


class Para(Abstract):
    def __init__(self, linea, columna, tipo_for, declaracion, condicion, expresion, sentencias):
        super().__init__(linea, columna)
        self.tipo_for = tipo_for
        self.declaracion = declaracion
        self.condicion = condicion
        self.expresion = expresion
        self.sentencias = sentencias

    def __str__(self):
        return f"Tipo -> Tipo for: {self.tipo_for}, Declaración: {self.declaracion}, Condición: {self.condicion}, Expresión: {self.expresion}, Sentencias: {self.sentencias}"

    def ejecutar(self, scope):
        if self.tipo_for == 1:
            print('Ejecutamos for tipo 1')
            scope_dentro_for: Scope = Scope(scope)
            self.declaracion.ejecutar(scope_dentro_for)
            self.sentencias.ejecutar(scope_dentro_for)
        else:
            print('Ejecutamos for tipo 2')
            scope_dentro_for: Scope = Scope(scope)
            self.declaracion.ejecutar(scope_dentro_for)
            self.sentencias.ejecutar(scope_dentro_for)

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        node = "nodo_" + subNameNode + "_" + nume
        decl = node + '[label = "<n>Para"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + node + ':n'))
        self.sentencias.graficar(scope, graphviz, subNameNode, node)
