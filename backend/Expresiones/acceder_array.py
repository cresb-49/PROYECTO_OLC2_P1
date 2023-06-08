from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class AccederArray(Abstract):
    def __init__(self, linea, columna, exprecion, index_exprecion):
        super().__init__(linea, columna)
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
                        print('El index debe ser un numero entero')
                else:
                    print('El index es mayor a size del array')
            else:
                print('El index debe de ser un: number')
        else:
            print('No esta operando un array')

    def graficar(self, scope, graphviz, subNameNode, padre):
        pass

    def convertir_float_a_int(self, numero_float):
        parte_decimal = numero_float % 1
        if parte_decimal == 0:
            return int(numero_float)
        else:
            return numero_float
