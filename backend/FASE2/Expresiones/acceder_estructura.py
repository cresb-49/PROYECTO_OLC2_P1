from FASE2.Abstract.abstract import Abstract
from FASE2.Abstract.return__ import Return
from FASE2.Symbol.tipoEnum import TipoEnum
from FASE2.Symbol.scope import Scope
from FASE2.Symbol.Exception import Excepcion
from FASE2.Symbol.generador import Generador


class AccederEstructura(Abstract):
    def __init__(self, resultado, linea, columna, id_acceso, parametro):
        super().__init__(resultado, linea, columna)
        self.id_acceso = id_acceso
        self.parametro = parametro

    def __str__(self):
        return f"AccederEstructura: id_acceso={self.id_acceso}, parametro={self.parametro}, linea={self.linea}, columna={self.columna}"

    def ejecutar(self, scope):
        resultado_id_acc = self.id_acceso.ejecutar(scope)
        if resultado_id_acc['tipo'] == TipoEnum.STRUCT:
            valor_recuperado = resultado_id_acc['value']
            if self.parametro in valor_recuperado:
                value_send = valor_recuperado[self.parametro]
                return value_send
            else:
                self.resultado.add_error(
                    'Semantico', f"El estruct \"{resultado_id_acc['tipo_secundario']}\" no tiene parametro \"{self.parametro}\"", self.linea, self.columna)
        else:
            self.resultado.add_error(
                'Semantico', f"La variable es de tipo: \"{resultado_id_acc['tipo'].value}\" no tiene parametros de acceso \"{self.parametro}\"", self.linea, self.columna)

    def graficar(self, graphviz, padre):
        result = graphviz.add_nodo('.', padre)
        graphviz.add_nodo(self.id_acceso, result)
        graphviz.add_nodo(self.parametro, result)

    def generar_c3d(self, scope: Scope):
        gen_aux = Generador()
        generador = gen_aux.get_instance()
        # print('Estoy en acceder estructura', type(self.id_acceso))
        # scope.imprimir()
        # Mandamos a traer la variable temporal de acceso del struct
        variable: Return = self.id_acceso.generar_c3d(scope)
        if isinstance(variable, Excepcion):
            return variable
        # Recuperamos la base del struct
        struct = scope.obtener_estructura(variable.aux_type)
        # print('Configuracion general struct: ', struct.configuracion)
        # Obtenemos la posicion del parametro segun base del struct
        param_stats = struct.configuracion[self.parametro]
        # print('Configuracion parametro struct: ', param_stats)
        generador.add_comment(f'Compilacion del acceso a un valor de struct variable {self.id_acceso.id}')
        param_struct = generador.add_temp()
        generador.add_exp(param_struct, variable.get_value(),
                          param_stats['pos'], '+')
        parametro = generador.add_temp()
        generador.get_heap(parametro, param_struct)
        generador.add_comment(f'Fin compilacion del acceso a un valor de struct variable {self.id_acceso.id}')
        result: Return = Return(parametro, param_stats['tipo'], True, param_stats['tipo_secundario'])
        return result
