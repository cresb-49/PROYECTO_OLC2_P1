from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class EstructuraVal(Abstract):
    def __init__(self, resultado, linea, columna, tipo_secundario, contenido):
        super().__init__(resultado, linea, columna)
        self.tipo = TipoEnum.STRUCT
        self.tipo_secundario = tipo_secundario
        self.contenido = contenido

    def __str__(self):
        return f"EstructuraVal: tipo={self.tipo}, tipo_secundario={self.tipo_secundario}, contenido={self.contenido}"
    
    def ejecutar(self, scope):
        pass

    def graficar(self, graphviz, padre):
        pass
