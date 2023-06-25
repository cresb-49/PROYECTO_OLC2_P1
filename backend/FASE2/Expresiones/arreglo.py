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
        print('DEBUJ ARRAY LARGO: ', largo)
        # Debemos sumar un espacio mas para tener el espacio a utilizar en el heap
        largo_final = largo + 1
        print('DEBUJ ARRAY ESPACIO HEAP: ', largo_final)
        generador.add_comment('Inicio compilacion de array')
        init_array = generador.add_temp()
        iterador = generador.add_temp()
        generador.add_asig(init_array, 'H')
        generador.add_exp(iterador, init_array, '1', '+')
        generador.set_heap('H', largo)
        generador.add_exp('H', 'H', str(largo_final), '+')

        tipo_array = ''
        for elemento in self.linealizado:
            elem: Return = elemento.generar_c3d(scope)
            if isinstance(elem, Excepcion):
                return elem
            if tipo_array == '':
                tipo_array = elem.get_tipo()
            if tipo_array != '':
                if tipo_array == elem.get_tipo():
                    generador.set_heap(iterador, elem.get_value())
                    # print('DEBUJ ARRAY TIPO ELEMENTO: ', tipo_array)
                    generador.add_exp(iterador, iterador, '1', '+')
                else:
                    concat = f'El tipo del array es {tipo_array.value} y esta agregando un {elem.get_tipo()}'
                    self.resultado.add_error(
                        'Semantico', concat, self.linea, self.columna)
                    return Excepcion('Semantico', concat, self.linea, self.columna)
        generador.add_comment('Fin compilacion de array')
        result: Return = Return(init_array, TipoEnum.ARRAY, True, tipo_array)
        result.dimenciones = self.dimenciones
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
        dimenciones = str(metadata).replace(' ', '').replace('(', '').replace(')', '').split(',')
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
