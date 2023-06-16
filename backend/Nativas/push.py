from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class Push(Abstract):
    def __init__(self, resultado, linea, columna, id_arreglo, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.id_arreglo = id_arreglo

    def __str__(self):
        return "Push"

    def verificar_tipos(array, param):
        if (array['tipo_secundario'] != None):
            if (array['tipo_secundario'] == param['tipo']):
                return True
            else:
                return False
        else:
            return False

    def ejecutar(self, scope):
        # Primero ejecutamos la base del nuevo arreglo
        result_id = self.id_arreglo.ejecutar(scope)
        if isinstance(result_id, dict):
            # Varificamos el tipo de variable que se ejecuto
            if result_id['tipo'] == TipoEnum.ARRAY:
                # Enviar ha ejecutar la exprecion para obtener su diccionario
                ejecucionDeExpresion = self.expreciones.ejecutar(scope)
                if (self.verificar_tipos(result_id, ejecucionDeExpresion)):
                    array = result_id['value']
                    param = ejecucionDeExpresion['value']
                    resultado_push = FuncionNativa.push(None, array, param)

                    if len(resultado_push) == 0:
                        return {"value": [], "tipo": result_id['tipo'], "tipo_secundario": result_id['tipo_secundario'], "linea": self.linea, "columna": self.columna}
                    else:
                        base = resultado_push[0]['tipo']
                        if all(base == exp['tipo'] for exp in resultado_push):
                            return {"value": resultado_push, "tipo": TipoEnum.ARRAY, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
                        else:
                            return {"value": resultado_push, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
                else:
                    self.resultado.add_error(
                        'Semantico', 'Tipos no coinciden', self.linea, self.columna)
                    return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                self.resultado.add_error(
                    'Semantico', 'push solo funciona con Arrays', self.linea, self.columna)
                return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            self.resultado.add_error(
                'Semantico', f'Concat, no se puede operar con el identificador {self.id_arreglo.id}', self.linea, self.columna)
            return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        # agregarmos el nombre del nodo (el de la operacion) y el nodo padre
        result = graphviz.add_nodo("toLowerCase", padre)
        # mandmaos ha graficar el hijo (acceder)
        self.numero.graficar(graphviz, result)
