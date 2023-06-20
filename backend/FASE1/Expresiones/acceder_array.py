from FASE1.Abstract.abstract import Abstract
from FASE1.Symbol.tipoEnum import TipoEnum


class AccederArray(Abstract):
    def __init__(self, resultado,linea, columna, exprecion, index_exprecion):
        super().__init__(resultado,linea, columna)
        self.exprecion = exprecion
        self.index_exprecion = index_exprecion

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        if result['tipo'] == TipoEnum.ARRAY:
            index = self.index_exprecion.ejecutar(scope)
            if index['tipo'] == TipoEnum.NUMBER:
                array = result['value']
                if index['value'] < len(array):
                    try:
                        return array[self.convertir_float_a_int(index['value'])]
                    except Exception:
                        self.resultado.add_error('Semantico', 'El index debe ser un numero entero', self.linea, self.columna)
                else:
                    self.resultado.add_error('Semantico', 'El index es mayor a size del array', self.linea, self.columna)
            else:
                self.resultado.add_error('Semantico', 'El index debe de ser un: number', self.linea, self.columna)
        else:
            self.resultado.add_error('Semantico', 'No esta operando un array', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        node_padre = graphviz.add_nodo('[]', padre)
        self.exprecion.graficar(graphviz, node_padre)
        self.index_exprecion.graficar(graphviz, node_padre)

    def convertir_float_a_int(self, numero_float):
        parte_decimal = numero_float % 1
        if parte_decimal == 0:
            return int(numero_float)
        else:
            return numero_float
        
    def generar_c3d(self,scope):
        pass