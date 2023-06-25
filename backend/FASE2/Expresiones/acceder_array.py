from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion


class AccederArray(Abstract):
    def __init__(self, resultado, linea, columna, exprecion, list_index_exprecion):
        super().__init__(resultado, linea, columna)
        self.exprecion = exprecion
        self.list_index_exprecion = list_index_exprecion

    def ejecutar(self, scope):
        result = self.exprecion.ejecutar(scope)
        return {"value": result['value'], "tipo": self.calculo_tipo(result['tipo_secundario']), "tipo_secundario": result['tipo_secundario'], "linea": self.linea, "columna": self.columna}

    def calculo_tipo(self, tipo):
        if isinstance(tipo, TipoEnum):
            return tipo
        else:
            return TipoEnum.STRUCT

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

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        print('DEBUJ ACCEDER ARRAY')
        # Ejecutamos la exprecion y verificamos que se de tipo ARRAY
        exprecion: Return = self.exprecion.generar_c3d(scope)
        if isinstance(exprecion, Excepcion):
            return exprecion
        if exprecion.get_tipo() == TipoEnum.ARRAY:
            if len(self.list_index_exprecion) == 1:
                index_result: Return = self.list_index_exprecion[0].generar_c3d(
                    scope)
                if isinstance(index_result, Excepcion):
                    return index_result
                if index_result.get_tipo() == TipoEnum.NUMBER:
                    inicio_array_heap = exprecion.get_value()
                    index = index_result.get_value()
                    print('DEBUJ ACCEDER INICIO ARRAY: ', exprecion)
                    size_array = generador.add_temp()
                    generador.get_heap(size_array, inicio_array_heap)
                    true_label = generador.new_label()
                    false_label = generador.new_label()
                    generador.add_if(index, size_array, '<', true_label)
                    generador.add_goto(false_label)
                    # Codigo Para acceder al array
                    generador.put_label(true_label)
                    pasos_array = generador.add_temp()
                    paso = generador.add_temp()
                    generador.add_exp(paso, index, '1', '+')
                    generador.add_exp(
                        pasos_array, inicio_array_heap, paso, '+')
                    valor_array = generador.add_temp()
                    generador.get_heap(valor_array, pasos_array)
                    generador.put_label(false_label)
                    # Funcion para que muestre error de parametros de acceso
                    return Return(valor_array, exprecion.get_tipo_aux(), True, None)
                else:
                    self.resultado.add_error(
                        'Semantico', 'El valor de acceso para el array debe se un numero', self.linea, self.columna)
                    return Excepcion('Semantico', 'El valor de acceso para el array debe se un numero', self.linea, self.columna)
            else:
                pass
        else:
            self.resultado.add_error(
                'Semantico', 'No esta operando un array', self.linea, self.columna)
            return Excepcion('Semantico', 'No esta operando un array', self.linea, self.columna)
