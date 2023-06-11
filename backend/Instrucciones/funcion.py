from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Funcion(Abstract):

    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, parametros, sentancias):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros
        self.tipo_secundario = tipo_secundario

    def __str__(self):
        return f"Funcion: {self.id}, tipo: {self.tipo}, tipo_secundario: {self.tipo_secundario}, parametros: {self.parametros}"

    def ejecutar(self, scope):
        if self.sentencias != None:
            result = self.sentencias.ejecutar(scope)
            if result != None:
                #Validar el tipo de retorno de la funcion
                return result                
            else:
                return {"value": '', "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            return {"value": '', "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        # TODO: Agregar la imprecion de los parametros
        graphviz.add_nodo('parametros', padre)
        graphviz.add_nodo(')', padre)
        graphviz.add_nodo('{', padre)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, padre)
        graphviz.add_nodo('}', padre)
