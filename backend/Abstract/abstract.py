from abc import ABC, abstractclassmethod


class Abstract(ABC):
    def __init__(self, linea, columna):
        super().__init__()
        self.linea = linea
        self.columna = columna

    @abstractclassmethod
    def ejecutar(self, scope):
        pass

    @abstractclassmethod
    def grficar(self, scope, graphviz, subNameNode, padre):
        pass
