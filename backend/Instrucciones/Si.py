from Abstracto.Instruccion import Instruccion
from Abstracto.Tipo import Tipo
from Abstracto.Tipo import TipoEnum
from Simbolo.Scope import Scope

class Si(Instruccion):
    def __init__(self, linea, columna, codeTrue, codeFalse):
        super().__init__(linea, columna)
        self.codeTrue = codeTrue
        self.codeFalse = codeFalse
        
    def ejecutar(self, scope: Scope) -> any:
        condicion = scope.obtenerVariable(self.identificador)
        if(condicion.tipo != TipoEnum.BOOLEAN):
             raise ValueError("La condicion de Si no es booleana Linea: " + self.linea + " ,Columna: " + self.columna)
        if(condicion.value):
            return self.codeTrue.ejecutar(scope)
        else:
            return self.codeFalse.ejecutar(scope)
        
   
    def graficar(self, scope, graphviz, padre):
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
             self.codeFalse.graficar(scope, graphviz, self.codeTrue, self.subNameNode, nodeSino)
        

  