from Abstract.abstract import Abstract


class Si(Abstract):
    def __init__(self, linea, columna, exprecion, sentencias, _else):
        super().__init__(linea, columna)
        self.exprecion = exprecion
        self.sentencias = sentencias
        self._else = _else

    def __str__(self):
        return f"If -> Expresión: {self.exprecion}, Sentencias: {self.sentencias}, Else: {self._else}"

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        if result:
            self.sentencias.ejecutar(scope)
        else:
            self._else.ejecutar(scope)

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
