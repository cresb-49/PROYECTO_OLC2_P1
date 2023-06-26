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
            generador.p_out_of_bouns()
            res = self.acceso_array_multidimencional(generador, scope, exprecion)
            if isinstance(res, Excepcion):
                return res
            valor = Return(res, exprecion.get_tipo_aux(), True, None)
            if exprecion.get_tipo_aux() != None:
                if not isinstance(exprecion.get_tipo_aux(),TipoEnum):
                    valor.set_tipo(TipoEnum.STRUCT)
                    valor.set_tipo_aux(exprecion.get_tipo_aux())
            return valor
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
        valor_heap = generador.add_temp()
        generador.get_heap(valor_heap, pos_heap)
        return valor_heap

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
