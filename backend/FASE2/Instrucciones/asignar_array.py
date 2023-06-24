from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion


class AsignacionArray(Abstract):
    def __init__(self, resultado, linea, columna, id_array, list_index_exprecion, value_exprecion):
        super().__init__(resultado, linea, columna)
        self.id_array = id_array
        self.index_exprecion = list_index_exprecion
        self.value_exprecion = value_exprecion

    def __str__(self):
        return f"Asignacion Array: {self.id_array}, index: {self.list_index_exprecion}, value: {self.value_exprecion}"

    def ejecutar(self, scope):
        # Ejecutamos primero el array? asi verificamos tipo e index
        result_array = self.array.ejecutar(scope)
        # Ejcutamos en index para utilizar en el array
        result_index = self.index_exprecion.ejecutar(scope)
        # Ejecutamos el value de la exprecion
        result_value = self.value_exprecion.ejecutar(scope)
        if result_array['tipo'] == TipoEnum.ARRAY:
            # Validacion del tipo secundario del array para ingresar el valor
            if result_array['tipo_secundario'] == TipoEnum.ANY.value:
                if result_index['tipo'] == TipoEnum.NUMBER:
                    index_agregate = result_index['value']
                    if index_agregate < len(result_array['value']):
                        try:
                            result_array['value'][self.convertir_float_a_int(
                                index_agregate)] = result_value
                        except Exception:
                            self.resultado.add_error(
                                'Semantico', 'El index debe ser un numero entero', self.linea, self.columna)
                    else:
                        self.resultado.add_error(
                            'Semantico', f'No existe un index {index_agregate} para el array a modificar', self.linea, self.columna)
                else:
                    self.resultado.add_error(
                        'Semantico', 'Para acceder a un array se necesita un index numerico', self.linea, self.columna)
            elif result_array['tipo_secundario'] == TipoEnum.STRUCT.value:
                print('####Asignacion a un array tipo struct')
            else:
                if result_index['tipo'] == TipoEnum.NUMBER:
                    index_agregate = result_index['value']
                    if index_agregate < len(result_array['value']):
                        if result_array['tipo_secundario'] == None:
                            print('Codigo incompleto asignar_array.py')
                            if len(result_array['value']) != 0:
                                self.resultado.add_error(
                                    'Semantico', 'La inicializacion del array esta vacia', self.linea, self.columna)
                            else:
                                self.resultado.add_error(
                                    'Semantico', 'No se sabe el tipo del array con el que se opera', self.linea, self.columna)
                        else:
                            # Validacion del tipo secundario
                            if result_array['tipo_secundario'] == TipoEnum.ANY.value:
                                try:
                                    result_array['value'][self.convertir_float_a_int(
                                        index_agregate)] = result_value
                                except Exception:
                                    self.resultado.add_error(
                                        'Semantico', 'El index debe ser un numero entero', self.linea, self.columna)
                            else:
                                if result_array['tipo_secundario'] == result_value['tipo'].value:
                                    try:
                                        result_array['value'][self.convertir_float_a_int(
                                            index_agregate)]['value'] = result_value['value']
                                    except Exception:
                                        self.resultado.add_error(
                                            'Semantico', 'El index debe ser un numero entero', self.linea, self.columna)
                                else:
                                    self.resultado.add_error(
                                        'Semantico', f'No se puede asignar un valor de tipo: {result_value["tipo"].value} al array', self.linea, self.columna)
                    else:
                        self.resultado.add_error(
                            'Semantico', f'No existe un index {index_agregate} para el array a modificar', self.linea, self.columna)
                else:
                    self.resultado.add_error(
                        'Semantico', 'Para acceder a un array se necesita un index numerico', self.linea, self.columna)
        else:
            self.resultado.add_error(
                'Semantico', f'No puede acceder a un index en un variable tipo: {result_array["tipo"].value}', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        igual = graphviz.add_nodo('=', padre)
        index = graphviz.add_nodo('[]', igual)
        self.array.graficar(graphviz, index)
        self.index_exprecion.graficar(graphviz,index)
        self.value_exprecion.graficar(graphviz, igual)

    def convertir_float_a_int(self, numero_float):
        parte_decimal = numero_float % 1
        if parte_decimal == 0:
            return int(numero_float)
        else:
            return numero_float

    def generar_c3d(self,scope:Scope):
        print('ASIGNAR VALOR ARRAY')
        # Obtenemos la variable del scope
        variable = scope.obtener_variable(self.id_array)
        # Verificamos que se ade tipo array
        if variable.tipo == TipoEnum.ARRAY:
            print('ARRAY: ',variable)
            
        else:
            self.resultado.add_error('Semantico', 'No esta operando un array', self.linea, self.columna)
            return Excepcion('Semantico', 'No esta operando un array', self.linea, self.columna)
        