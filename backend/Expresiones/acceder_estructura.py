from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


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
