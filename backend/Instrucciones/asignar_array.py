from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class AsignacionArray(Abstract):
    def __init__(self, resultado, linea, columna, array, index_exprecion, value_exprecion):
        super().__init__(resultado, linea, columna)
        self.array = array
        self.index_exprecion = index_exprecion
        self.value_exprecion = value_exprecion

    def __str__(self):
        return f"Asignacion Array: {self.array}, index: {self.index_exprecion}, value: {self.value_exprecion}"

    def ejecutar(self, scope):
        # Ejecutamos primero el array? asi verificamos tipo e index
        result_array = self.array.ejecutar(scope)
        #Ejcutamos en index para utilizar en el array
        result_index = self.index_exprecion.ejecutar(scope)
        #Ejecutamos el value de la exprecion
        result_value = self.value_exprecion.ejecutar(scope)
        
        if result_array['tipo'] == TipoEnum.ARRAY:
            # Validacion del tipo secundario del array para ingresar el valor
            if result_array['tipo_secundario'] == TipoEnum.ANY.value:
                print('Asignacion a un array tipo any')
            elif result_array['tipo_secundario'] == TipoEnum.STRUCT.value:
                print('Asignacion a un array tipo struct')
            else:
                if result_index['tipo'] == TipoEnum.NUMBER:
                    index_agregate = result_index['value']
                    if index_agregate < len(result_array['value']):    
                        if result_array['tipo_secundario'] == None:
                            print('Codigo incompleto asignar_array.py')
                            if len(result_array['value']) != 0:
                                self.resultado.add_error('Semantico', 'La inicializacion del array esta vacia', self.linea, self.columna)
                            else:
                                self.resultado.add_error('Semantico', 'No se sabe el tipo del array con el que se opera', self.linea, self.columna)
                        else:
                            #Validacion del tipo secundario
                            if result_array['tipo_secundario'] == TipoEnum.ANY.value:
                                print('Valor asignar ->',result_value)
                            else:
                                if result_array['tipo_secundario'] == result_value['tipo'].value:
                                    pass
                                else:
                                    self.resultado.add_error('Semantico', f'No se puede asignar un valor de tipo {result_value["tipo"].value} para el array a modificar', self.linea, self.columna)                  
                    else:
                        self.resultado.add_error('Semantico', f'No existe un index {index_agregate} para el array a modificar', self.linea, self.columna)      
                else:
                    self.resultado.add_error('Semantico', 'Para acceder a un array se necesita un index numerico', self.linea, self.columna)        
        else:
            self.resultado.add_error(
                'Semantico', f'No puede acceder a un index en un variable tipo: {result_array["tipo"].value}', self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo(self.id, padre)
        igual = graphviz.add_nodo('=', result)
        self.valor.graficar(graphviz, igual)
