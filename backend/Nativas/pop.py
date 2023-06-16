from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class Pop(Abstract):
    def __init__(self, resultado, linea, columna, id_arreglo, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.id_arreglo = id_arreglo

    def __str__(self):
        return "Pop"

    def verificar_tipos(self, array, param):
        if (array['tipo_secundario'] != None):
            if(array['tipo_secundario'] == 'any'):
                 return True
            elif (array['tipo_secundario'] == param['tipo'].value):
                return True
            else:
                return False
        else:
            if (array['tipo'] == param['tipo']):
                return True
            else:
                return False

    def verificar_length(self, array, param):
        if (len(array) - 1 >= param):
            return True
        else:
            return False

    def ejecutar(self, scope):
        # Primero ejecutamos la base del nuevo arreglo
        result_id = self.id_arreglo.ejecutar(scope)
        if isinstance(result_id, dict):
            # Varificamos el tipo de variable que se ejecuto
            if result_id['tipo'] == TipoEnum.ARRAY:
                # Enviar ha ejecutar la exprecion para obtener su diccionario
                ejecucionDeExpresion = self.expreciones.ejecutar(scope)
                if (self.verificar_tipos(result_id, ejecucionDeExpresion)):

                    array = result_id['value']
                    param = ejecucionDeExpresion['value']
                    if (self.verificar_length(array, param)):
                        FuncionNativa.pop(None, array, param)
                    else:
                        self.resultado.add_error(
                            'Semantico', 'Index fuera del alcance del Array', self.linea, self.columna)
                else:
                    self.resultado.add_error(
                        'Semantico', 'Tipos no coinciden', self.linea, self.columna)
            else:
                self.resultado.add_error(
                    'Semantico', 'push solo funciona con Arrays', self.linea, self.columna)
        else:
            self.resultado.add_error(
                'Semantico', f'Concat, no se puede operar con el identificador {self.id_arreglo.id}', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("Pop", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.expreciones.graficar(graphviz, result)

    def generar_c3d(self, scope):
        pass
