from Abstract.abstract import Abstract
from Modulos.funcion_nativa import FuncionNativa
from Symbol.tipoEnum import TipoEnum


class Concat(Abstract):
    def __init__(self, resultado, linea, columna, id_arreglo, expreciones):
        super().__init__(resultado, linea, columna)
        self.expreciones = expreciones
        self.id_arreglo = id_arreglo

    def __str__(self):
        return "Concat"

    def ejecutar(self, scope):
        # Primero ejecutamos la base del nuevo arreglo
        result_id = self.id_arreglo.ejecutar(scope)
        if isinstance(result_id, dict):
            # Varivicamos el tipo de variable que se ejecuto
            if result_id['tipo'] == TipoEnum.ARRAY:
                # Ejecutamos la exprecion de entrada
                val_concat = self.expreciones.ejecutar(scope)
                # Verificamos que la entrada tambien sea un array
                if val_concat['tipo'] == TipoEnum.ARRAY:
                    resultado_concat = result_id['value'] + val_concat['value']
                    if len(resultado_concat) == 0:
                        return {"value": [], "tipo": result_id['tipo'], "tipo_secundario": result_id['tipo_secundario'], "linea": self.linea, "columna": self.columna}
                    else:
                        base = resultado_concat[0]['tipo']
                        if all(base == exp['tipo'] for exp in resultado_concat):
                            return {"value": resultado_concat, "tipo": TipoEnum.ARRAY, "tipo_secundario": base.value, "linea": self.linea, "columna": self.columna}
                        else:
                            return {"value": resultado_concat, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
                else:
                    self.resultado.add_error(
                        'Semantico', 'concat solo funciona con un array en la entrada', self.linea, self.columna)
                    return {"value": None, "tipo": TipoEnum.ERROR, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
            else:
                self.resultado.add_error(
                    'Semantico', 'concat solo funciona con Arrays', self.linea, self.columna)
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

    def generar_c3d(self,scope):
        pass