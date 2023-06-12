from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Acceder(Abstract):
    def __init__(self, resultado, linea, columna, id):
        super().__init__(resultado, linea, columna)
        self.id = id

    def ejecutar(self, scope):
        recuperacion = scope.obtener_variable(self.id)
        if (recuperacion == None):
            self.resultado.add_error(
                'Semantico', f"La variable {self.id} no existe", self.linea, self.columna)
        else:
            if (recuperacion.tipo == TipoEnum.ANY):
                if recuperacion.tipo_secundario == TipoEnum.NUMBER.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.NUMBER, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.BOOLEAN.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.BOOLEAN, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.STRING.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.STRING, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.STRUCT.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.STRUCT, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.ARRAY.value:
                    # Se debe realizar el calculo de tipo para el regreso
                    if len(recuperacion.valor) != 0:
                        base = recuperacion.valor[0]['tipo']
                        if all(base == exp['tipo'] for exp in recuperacion.valor):
                            tipo_secundario = base.value
                            return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": tipo_secundario, "linea": self.linea, "columna": self.columna}
                        else:
                            return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": TipoEnum.ANY.value, "linea": self.linea, "columna": self.columna}
                    else:
                        return {"value": [], "tipo": TipoEnum.ARRAY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                elif recuperacion.tipo_secundario == TipoEnum.ANY.value:
                    return {"value": recuperacion.valor, "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                print('No devolvio nada acceder')
            elif (recuperacion.tipo == TipoEnum.ARRAY):
                return {"value": recuperacion.valor, "tipo": TipoEnum.ARRAY, "tipo_secundario": recuperacion.tipo_secundario, "linea": self.linea, "columna": self.columna}
            else:
                return {"value": recuperacion.valor, "tipo": recuperacion.tipo, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
