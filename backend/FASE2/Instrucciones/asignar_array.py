from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion
from FASE2.Expresiones.acceder import Acceder


class AsignacionArray(Abstract):
    def __init__(self, resultado, linea, columna, id_array, list_index_exprecion, value_exprecion):
        super().__init__(resultado, linea, columna)
        self.id_array = id_array
        self.list_index_exprecion = list_index_exprecion
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
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        generador.add_comment('Compilacion de asignar valor a espacio de array')
        acceder:Acceder = Acceder(self.resultado,self.linea,self.columna,self.id_array)
        # Obtenemos el puntero del heap del array 
        result2:Return = acceder.generar_c3d(scope)
        if isinstance(result2,Excepcion): return result2
        # Verificamos que se ade tipo array
        if result2.get_tipo() == TipoEnum.ARRAY:
            # Obtenemos el valor a asignar
            result:Return = self.value_exprecion.generar_c3d(scope)
            if isinstance(result,Excepcion): return result
            # Validacion en del tipo de dato en la entrada del array
            if result.get_tipo() == result2.get_tipo_aux():
                generador.p_out_of_bouns()
                pos_heap = self.acceso_array_multidimencional(generador,scope,result2)
                if isinstance(pos_heap,Excepcion): return pos_heap
                # Asignacion de valor en la posicion del heap del array 
                generador.set_heap(pos_heap,result.get_value())
            else:
                error = f'El array "{self.id_array}" es de tipo {result2.get_tipo_aux()} y esta asignando un valor de tipo {result.get_tipo()}'
                self.resultado.add_error('Semantico', error, self.linea, self.columna)
                return Excepcion('Semantico', error, self.linea, self.columna)
        else:
            self.resultado.add_error('Semantico', 'No esta operando un array', self.linea, self.columna)
            return Excepcion('Semantico', 'No esta operando un array', self.linea, self.columna)
    
    def acceso_array_multidimencional(self, generador: Generador, scope: Scope, exprecion: Return):
        generador.add_comment('Compilacion de las expreciones para utilizarlas en las operaciones de acceso')
        index_compilados = []
        for index_exp in self.list_index_exprecion:
            result: Return = index_exp.generar_c3d(scope)
            if isinstance(result, Excepcion):
                return result
            index_compilados.append(result)
        return self.validacion_accesos(generador, index_compilados, exprecion)

    def validacion_accesos(self, generador: Generador, index_compilados, exprecion: Return):
        puntero_heap = exprecion.get_value()
        print(puntero_heap)
        generador.add_comment('Cantidad de dimenciones del array')
        cantidad_dimenciones = generador.add_temp()
        # Variable temporal que alamecena la posicion el heap para realizar los calculos
        pos_heap = generador.add_temp()
        generador.add_exp(pos_heap, puntero_heap, '1', '+')
        generador.get_heap(cantidad_dimenciones, pos_heap)
        generador.add_comment('Validacion de acceso a dimenciones')
        t_label = generador.new_label()
        false_label = generador.new_label()
        generador.add_if(len(index_compilados),
                         cantidad_dimenciones, '<=', t_label)
        generador.add_goto(false_label)
        generador.put_label(t_label)
        generador.add_comment('Validacion size de cada dimencion')
        cont = 2
        for index in index_compilados:
            true_label = generador.new_label()
            pos_size_dimencion = generador.add_temp()
            generador.add_exp(pos_heap, puntero_heap, cont, '+')
            generador.get_heap(pos_size_dimencion, pos_heap)
            generador.add_if(index.get_value(),
                             pos_size_dimencion, '<', true_label)
            generador.add_goto(false_label)
            generador.put_label(true_label)
            cont += 1
        salto_error = generador.new_label()
        generador.add_goto(salto_error)
        generador.put_label(false_label)
        generador.call_fun('outOfBounds')
        #generador.add_goto_out()
        generador.put_label(salto_error)
        generador.add_comment('Calculo de acceso al array')
        # Logica para el calculo del index
        index_array = self.generacion_pos_recursiva(
            generador, index_compilados, puntero_heap)
        generador.add_comment('Calculo de la posicion en el heap')
        # Calculo en la ubicacion en el heap del dato del array
        # Se le suma dos para la posicion del tamanio y de la cantidad de dimenciones del array
        generador.add_exp(pos_heap, puntero_heap, '2', '+')
        # Sumamos la cantidad de dimenciones ya que es la cantidad de espacios a correr
        generador.add_exp(pos_heap, pos_heap, cantidad_dimenciones, '+')
        # Ahora sumamos la posicion que tiene en el array el elemento
        generador.add_exp(pos_heap, pos_heap, index_array, '+')
        return pos_heap

    def generacion_pos_recursiva(self, generador: Generador, index_compilados, puntero_heap):
        # Variable temporal que alamecena la posicion el heap para realizar los calculos
        pos_heap = generador.add_temp()
        contador = 0
        pos = 2
        heredado = ''
        for index in index_compilados:
            if contador == 0:
                temp = generador.add_temp()
                generador.add_exp(temp, index.get_value(), '0', '-')
                heredado = temp
            else:
                temp1 = generador.add_temp()
                size = generador.add_temp()
                generador.add_exp(pos_heap, puntero_heap, pos, '+')
                generador.get_heap(size, pos_heap)
                generador.add_exp(temp1, heredado, size, '*')
                temp2 = generador.add_temp()
                generador.add_exp(temp2, temp1, index.get_value(), '+')
                temp3 = generador.add_temp()
                generador.add_exp(temp3, temp2, 0, '-')
                heredado = temp3
            contador += 1
            pos += 1
        return heredado