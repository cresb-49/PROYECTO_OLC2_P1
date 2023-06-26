from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.Exception import Excepcion
import numpy


class Arreglo(Abstract):
    def __init__(self, resultado, linea, columna, tipo, tipo_secundario, arreglo):
        super().__init__(resultado, linea, columna)
        self.tipo = tipo
        self.tipo_secundario = tipo_secundario
        self.arreglo = arreglo
        self.dimenciones = []
        self.linealizado = []

    def ejecutar(self, scope):
        results = []
        for parte in self.arreglo:
            resultado = parte.ejecutar(scope)
            results.append(resultado)

        if len(results) > 0:
            base = results[0]['tipo']
            if all(base == exp['tipo'] for exp in results):
                tipo_secundario = base.value
                return {"value": results, "tipo": self.tipo, "tipo_secundario": tipo_secundario, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": results, "tipo": self.tipo, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
        else:
            return {"value": results, "tipo": self.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        node_padre = graphviz.add_nodo('[]', padre)
        for parte in self.arreglo:
            parte.graficar(graphviz, node_padre)

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        print('generando c3d array')
        # calculamos el largo del array
        result = self.calculo_caracteristicas_array()
        if isinstance(result, Excepcion):
            return result
        largo = len(self.linealizado)
        print('DEBUJ CANTIDAD ELEMENTOS: ', largo)
        dimenciones = len(self.dimenciones)
        print('DEBUJ ARRAY DIMENCIONES: ', dimenciones)
        cont = 0
        for dim in self.dimenciones:
            cont += 1
            print(f'VALOR DIMENCION {cont}: ', dim)
        # El largo representa que informacion del array de la siguinte forma
        # largo_final = un_espacio_para_largo + un_espacio_cantidad_dimenciones + (tamanios_cada_dimencion) + cantidad_datos
        largo_final = 1 + 1 + cont + largo
        print('CANTIDAD DE ESPACIO A RESERVAR: ', largo_final)
        generador.add_comment('Inicio compilacion de array')
        init_array = generador.add_temp()
        iterador = generador.add_temp()
        generador.add_asig(init_array, 'H')
        generador.add_exp(iterador, init_array, '1', '+')
        generador.add_comment('Cantidad de elementos')
        generador.set_heap('H', largo)
        generador.add_exp('H', 'H', str(largo_final), '+')
        generador.add_comment('Cantidad de dimenciones del array')
        generador.set_heap(iterador, dimenciones)
        generador.add_exp(iterador, iterador, '1', '+')
        # Ciclo de ingreso del size de cada dimencion del array
        generador.add_comment('Size de cada dimencion')
        for size_dim in self.dimenciones:
            generador.set_heap(iterador, size_dim)
            generador.add_exp(iterador, iterador, '1', '+')
        # Ingreso de los valores al array
        generador.add_comment('Elementos del array')
        tipo_array = ''
        for elemento in self.linealizado:
            elem: Return = elemento.generar_c3d(scope)
            if isinstance(elem, Excepcion):
                return elem
            if tipo_array == '':
                if elem.get_tipo() == TipoEnum.STRUCT:
                    tipo_array = elem.get_tipo_aux()
                else:
                    tipo_array = elem.get_tipo()
            if tipo_array != '':
                if elem.get_tipo() == TipoEnum.STRUCT:
                    if elem.get_tipo_aux() == tipo_array:
                        generador.set_heap(iterador, elem.get_value())
                        generador.add_exp(iterador, iterador, '1', '+')
                    else:
                        concat = f'El tipo del array es {tipo_array} y esta agregando un {elem.get_tipo_aux()}'
                        self.resultado.add_error('Semantico', concat, self.linea, self.columna)
                        return Excepcion('Semantico', concat, self.linea, self.columna)
                elif tipo_array == elem.get_tipo():
                    generador.set_heap(iterador, elem.get_value())
                    generador.add_exp(iterador, iterador, '1', '+')
                else:
                    concat = ''
                    if isinstance(tipo_array,TipoEnum):
                        concat = f'El tipo del array es {tipo_array.value} y esta agregando un {elem.get_tipo()}'
                    else:
                        concat = f'El tipo del array es {tipo_array} y esta agregando un {elem.get_tipo()}'
                    self.resultado.add_error('Semantico', concat, self.linea, self.columna)
                    return Excepcion('Semantico', concat, self.linea, self.columna)
        generador.add_comment('Fin elementos array')
        result: Return = Return(init_array, TipoEnum.ARRAY, True, tipo_array)
        result.dimenciones = self.dimenciones
        generador.add_comment('Fin compilacion de array')
        print('Tipos del array: ', result)
        return result

    def calculo_caracteristicas_array(self):
        # Linealizacion del array
        lienalizado = []
        for elemento in self.arreglo:
            if isinstance(elemento, Arreglo):
                self.linealizacion(lienalizado, elemento)
            else:
                lienalizado.append(elemento)
        des_encriptado = []
        for elemento in self.arreglo:
            if isinstance(elemento, Arreglo):
                des_encriptado.append(self.sub_array(elemento))
            else:
                des_encriptado.append(elemento)
        # print('Array desencriptado: ', des_encriptado)
        metadata = ''
        try:
            metadata = numpy.shape(des_encriptado)
        except ValueError as e:
            self.resultado.add_error(
                'Semantico', 'Esta declarando un array que no es homogeneo sus dimenciones deben ser simetricas', self.linea, self.columna)
            return Excepcion('Semantico', 'Esta declarando un array que no es homogeneo sus dimenciones deben ser simetricas', self.linea, self.columna)
        dimenciones = str(metadata).replace(' ', '').replace(
            '(', '').replace(')', '').split(',')
        if '' in dimenciones:
            dimenciones.remove('')
        # print('dimenciones: ', dimenciones)
        self.dimenciones = dimenciones
        self.linealizado = lienalizado

    def linealizacion(self, array, sub_array):
        for elemento in sub_array.arreglo:
            if isinstance(elemento, Arreglo):
                self.linealizacion(array, elemento)
            else:
                array.append(elemento)

    def sub_array(self, exprecion):
        des_encriptado = []
        for elemento in exprecion.arreglo:
            if isinstance(elemento, Arreglo):
                des_encriptado.append(self.sub_array(elemento))
            else:
                des_encriptado.append(elemento)
        return des_encriptado
