from Abstract.abstract import Abstract
from Symbol.scope import Scope
from Symbol.tipoEnum import TipoEnum


class Si(Abstract):
    def __init__(self, resultado, linea, columna, exprecion, sentencias, _else):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion
        self.sentencias = sentencias
        self._else = _else

    def __str__(self):
        return f"If -> Expresión: {self.exprecion}, Sentencias: {self.sentencias}, Else: {self._else}"

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        try:
            if result['tipo'] == TipoEnum.BOOLEAN:
                if result['value']:
                    print('If -> Verdadero')
                    if self.sentencias != None:
                        new_scope = Scope(scope)
                        return self.sentencias.ejecutar(new_scope)
                else:
                    print('If -> Falso')
                    if self._else != None:
                        new_scope = Scope(scope)
                        return self._else.ejecutar(new_scope)
            else:
                print('Error el if opera con una exprecion booleana')
        except Exception:
            print('No se puede operar la sentencia existe un error anterior')

    def graficar(self, scope, graphviz, subNameNode, padre):
        nume = graphviz.declaraciones.length + 1
        nodeSi = "nodo_" + self.subNameNode + "_" + nume
        decl = nodeSi + '[label = "<n>Si"];'
        graphviz.declaraciones.push(decl)
        graphviz.relaciones.push((padre + ':n -> ' + nodeSi + ':n'))
        self.codeTrue.graficar(scope, graphviz, self.subNameNode, nodeSi)
        if (self.codeFalse != None):
            nume = graphviz.declaraciones.length + 1
            nodeSino = "nodo_" + self.subNameNode + "_" + nume
            decl = nodeSino + '[label = "<n>Sino"];'
            graphviz.declaraciones.push(decl)
            graphviz.relaciones.push((nodeSi + ':n -> ' + nodeSino + ':n'))
            self.codeFalse.graficar(
                scope, graphviz, self.codeTrue, self.subNameNode, nodeSino)
