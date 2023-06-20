from FASE2.Abstract.abstract import Abstract
from FASE2.Symbol.tipoEnum import TipoEnum


class Estructura(Abstract):
    def __init__(self, resultado, linea, columna, id, composicion):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.composicion = composicion

    def __str__(self):
        return f"Struct: id={self.id}, composicion={self.composicion}"

    def ejecutar(self, scope):
        pass

    def graficar(self, graphviz, padre):
        pass
    
    def generar_c3d(self,scope):
        pass