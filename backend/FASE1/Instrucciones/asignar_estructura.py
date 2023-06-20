from FASE1.Abstract.abstract import Abstract
from FASE1.Symbol.tipoEnum import TipoEnum


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
                        tipo_secundario_original = ((struct_respectivo.composicion)[self.parametro])['tipo_secundario']
                        tipo_secundario_calculado = self.calcular_tipo_array(valor_asignar)
                        if tipo_secundario_original == tipo_secundario_calculado:
                            valor_recuperado[self.parametro] = valor_asignar    
                        else:
                            self.resultado.add_error('Semantico', f"El parametro \"{self.parametro}\" del estruct solo puede contener valores de tipo: \"{tipo_secundario_original}\" y esta asignando un valor de tipo: \"{tipo_secundario_calculado}\"", self.linea, self.columna)
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

    def generar_c3d(self,scope):
        pass