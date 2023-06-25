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
                    generador.p_out_of_bouns()
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
                    salto_error = generador.new_label()
                    generador.add_goto(salto_error)
                    generador.put_label(false_label)
                    generador.call_fun('outOfBounds')
                    generador.add_goto_out()
                    generador.put_label(salto_error)
                    # Funcion para que muestre error de parametros de acceso
                    return Return(valor_array, exprecion.get_tipo_aux(), True, None)
                else:
                    self.resultado.add_error(
                        'Semantico', 'El valor de acceso para el array debe se un numero', self.linea, self.columna)
                    return Excepcion('Semantico', 'El valor de acceso para el array debe se un numero', self.linea, self.columna)
            else:
                generador.p_out_of_bouns()
                res = self.acceso_array_multidimencional(
                    generador, scope, exprecion)
                if isinstance(res, Excepcion):
                    return res
        else:
            self.resultado.add_error(
                'Semantico', 'No esta operando un array', self.linea, self.columna)
            return Excepcion('Semantico', 'No esta operando un array', self.linea, self.columna)

    def acceso_array_multidimencional(self, generador: Generador, scope: Scope, exprecion: Return):
        generador.add_comment(
            'Compilacion de las expreciones para utilizarlas en las operaciones de acceso')
        index_compilados = []
        for index_exp in self.list_index_exprecion:
            result: Return = index_exp.generar_c3d(scope)
            if isinstance(result, Excepcion):
                return result
            index_compilados.append(result)
        for compilado in index_compilados:
            print(type(compilado))
        self.validacion_accesos(generador, index_compilados, exprecion)
        return Excepcion('Prubebas', 'pruebas de acceder array', self.linea, self.columna)

    def validacion_accesos(self, generador: Generador, index_compilados, exprecion: Return):
        if len(index_compilados) != len(exprecion.dimenciones):
            self.resultado.add_error(
                'Semantico', f'El array al cual quiere acceder es de: {len(exprecion.dimenciones)} dimenciones y su instruccion de acceso es de: {len(index_compilados)} dimenciones', self.linea, self.columna)
            return Excepcion('Semantico', f'El array al cual quiere acceder es de: {len(exprecion.dimenciones)} dimenciones y su intruccion de acceso es de: {len(index_compilados)} dimenciones', self.linea, self.columna)
        false_label = generador.new_label()
        for index, size in zip(index_compilados, exprecion.dimenciones):
            true_label = generador.new_label()
            generador.add_if(index.get_value(), size, '<', true_label)
            generador.add_goto(false_label)
            generador.put_label(true_label)
            print(size)
            print(index.get_value())

        salto_error = generador.new_label()
        generador.add_goto(salto_error)
        generador.put_label(false_label)
        generador.call_fun('outOfBounds')
        generador.add_goto_out()
        generador.put_label(salto_error)
        # Logica para el calculo del index
        self.generacion_pos_recursiva(generador,index_compilados, exprecion)

    def generacion_pos_recursiva(self,generador:Generador, index_compilados, exprecion):
        contador = 0
        heredado = ''
        for index, size in zip(index_compilados, exprecion.dimenciones):
            if contador == 0:
                temp = generador.add_temp()
                generador.add_exp(temp,index.get_value(),'0','-')
                heredado = temp
            else:
                temp1 = generador.add_temp()
                generador.add_exp(temp1,heredado,size,'*')
                temp2 = generador.add_temp()
                generador.add_exp(temp2,temp1,index.get_value(),'+')
                temp3 = generador.add_temp()
                generador.add_exp(temp3,temp2,0,'-')
                heredado = temp3
            contador += 1
        print('resultado Final: ',heredado)
        generador.add_debuj('f',heredado)
