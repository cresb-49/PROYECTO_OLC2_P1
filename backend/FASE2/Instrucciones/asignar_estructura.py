from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.generador import Generador
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion


class AsignacionEstructura(Abstract):
    def __init__(self, resultado, linea, columna, id, parametro, expresion):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.parametro = parametro
        self.expresion = expresion

    def __str__(self):
        return f"AsignacionEstructura: id={self.id}, parametro={self.parametro}, expresion={self.expresion}, linea={self.linea}, columna={self.columna}"

    def ejecutar(self, scope):
        var_acceso = self.id.ejecutar(scope)
        if var_acceso['tipo'] == TipoEnum.STRUCT:
            valor_recuperado = var_acceso['value']
            if self.parametro in valor_recuperado:
                # Ejecutamos la exprecion y validamos que ese sea el parametro de entrada
                valor_asignar = self.expresion.ejecutar(scope)
                struct_respectivo = scope.obtener_estructura(
                    var_acceso['tipo_secundario'])
                tipo_referencia = ((struct_respectivo.composicion)[
                                   self.parametro])['tipo']
                if tipo_referencia == TipoEnum.ANY or tipo_referencia == valor_asignar['tipo']:
                    if tipo_referencia == TipoEnum.ARRAY:
                        tipo_secundario_original = ((struct_respectivo.composicion)[
                                                    self.parametro])['tipo_secundario']
                        tipo_secundario_calculado = self.calcular_tipo_array(
                            valor_asignar)
                        if tipo_secundario_original == tipo_secundario_calculado:
                            valor_recuperado[self.parametro] = valor_asignar
                        else:
                            self.resultado.add_error(
                                'Semantico', f"El parametro \"{self.parametro}\" del estruct solo puede contener valores de tipo: \"{tipo_secundario_original}\" y esta asignando un valor de tipo: \"{tipo_secundario_calculado}\"", self.linea, self.columna)
                    else:
                        valor_recuperado[self.parametro] = valor_asignar
                else:
                    self.resultado.add_error(
                        'Semantico', f"El parametro \"{self.parametro}\" del estruct solo puede contener valores de tipo: \"{tipo_referencia.value}\" y esta asignando un valor de tipo: \"{valor_asignar['tipo'].value}\"", self.linea, self.columna)
            else:
                self.resultado.add_error(
                    'Semantico', f"El estruct \"{var_acceso['tipo_secundario']}\" no tiene parametro \"{self.parametro}\"", self.linea, self.columna)
        else:
            self.resultado.add_error(
                'Semantico', f"La variable es de tipo: \"{var_acceso['tipo'].value}\" no tiene parametros de acceso \"{self.parametro}\"", self.linea, self.columna)

    def graficar(self, graphviz, padre):
        node_equal = graphviz.add_nodo('=', padre)
        node_dot = graphviz.add_nodo('.', node_equal)
        graphviz.add_nodo(self.id, node_dot)
        graphviz.add_nodo(self.parametro, node_dot)
        self.expresion.graficar(graphviz, node_equal)

    def calcular_tipo_array(self, array):
        tipo_secundario = array['tipo_secundario']
        print(tipo_secundario)
        if tipo_secundario != None:
            return tipo_secundario
        else:
            print('Realizar el calculo del tipo de array')
            return None

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        print('Asignacion parametro estructura')
        # Al ser un struct los valores que ingresemos aqui deben agregarse
        # a la posicion en el heap segun la recuperacion

        generador.add_comment('Compilacion de asignacion de valor a estruct')
        # Primero obtenemos los parametros de acceso
        variable: Return = self.id.generar_c3d(scope)
        if (isinstance(variable, Excepcion)):
            return variable
        print('Varible estruct->', variable)
        print('Parametro a buscar ->', self.parametro)
        # Buscamos la base del struct para realizar buscar su configuracion
        struct = scope.obtener_estructura(variable.aux_type)
        if struct == None:
            generador.add_comment('Fin compilacion de asignacion de valor a estruct')
            self.resultado.add_error('Semantico', f'No existe la estructura {variable.aux_type}', self.linea, self.columna)
            return Excepcion('Semantico', f'No existe la estructura {variable.aux_type}', self.linea, self.columna)
        # Verificamos que el parametro existe en el struct
        if self.parametro in struct.configuracion:
            config = struct.configuracion[self.parametro]
            print('Estructura base: ',config)
            generador.add_comment('Recuperacion del puntero del Heap del stack')
            pos_heap = generador.add_temp();
            generador.add_exp(pos_heap,variable.get_value(),config['pos'],'+')
            asignacion:Return = self.expresion.generar_c3d(scope)
            if (isinstance(asignacion, Excepcion)):
                return asignacion
            # Verificamos que el tipo que vamos a asignar al valor del struct sea el correcto
            if config['is_mutable']:
                #print('====> el parametro es mutable',config)
                #print('====> el parametro es mutable',asignacion)
                config['tipo'] = asignacion.type
                config['tipo_secundario'] = asignacion.aux_type
                # Aqui debemos de realizar el set heap del valor nuevo
                generador.set_heap(pos_heap,asignacion.get_value())
            elif config['tipo'] == asignacion.type:
                print('Valor asignacion: ',asignacion)    
                # Aqui debemos de realizar el set heap del valor nuevo
                generador.set_heap(pos_heap,asignacion.get_value())
            else:
                self.resultado.add_error('Semantico', f'Al parametro {self.parametro} de tipo: {config["tipo"].value}, no se le puede asignar un: {asignacion.type.value}', self.linea, self.columna)
                return Excepcion('Semantico', f'Al parametro {self.parametro} de tipo: {config["tipo"].value}, no se le puede asignar un: {asignacion.type.value}', self.linea, self.columna)
            generador.add_comment('Fin compilacion de asignacion de valor a estruct')
        else:
            generador.add_comment('Fin compilacion de asignacion de valor a estruct')
            self.resultado.add_error('Semantico', f'No existe el parametro "{self.parametro}" en la estructura "{variable.aux_type}"', self.linea, self.columna)
            return Excepcion('Semantico', f'No existe el parametro "{self.parametro}" en la estructura "{variable.aux_type}"', self.linea, self.columna)