from abc import ABC, abstractclassmethod

class Abstract(ABC):
    def __init__(self, resultado,linea, columna):
        super().__init__()
        self.linea = linea
        self.columna = columna
        self.resultado = resultado

    @abstractclassmethod
    def ejecutar(self, scope):
        pass

    @abstractclassmethod
    def graficar(self, scope, graphviz, subNameNode, padre):
        pass
