from Abstract.abstract import Abstract
from Symbol.tipoEnum import TipoEnum


class Funcion(Abstract):

    def __init__(self, resultado, linea, columna, id, tipo, tipo_secundario, parametros, sentancias):
        super().__init__(resultado, linea, columna)
        self.id = id
        self.tipo = tipo
        self.sentencias = sentancias
        self.parametros = parametros
        self.tipo_secundario = tipo_secundario

    def __str__(self):
        return f"Funcion: {self.id}, tipo: {self.tipo}, tipo_secundario: {self.tipo_secundario}, parametros: {self.parametros}"

    def ejecutar(self, scope):
        if self.sentencias != None:
            result = self.sentencias.ejecutar(scope)
            print('debuj funcion',result)
            if self.validacion_salida_funccion(result):
                if result != None:
                    # Validar el tipo de retorno de la funcion
                    return result
                else:
                    if self.tipo == TipoEnum.ARRAY or self.tipo == TipoEnum.BOOLEAN or self.tipo == TipoEnum.NUMBER or self.tipo == TipoEnum.STRING or self.tipo == TipoEnum.STRUCT:
                        self.resultado.add_error(
                            'Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} agregue la instruccion', self.linea, self.columna)
                        return {"value": 'Null', "tipo": TipoEnum.NULL, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
                    else:
                        return {"value": '', "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}
        else:
            return {"value": '', "tipo": TipoEnum.ANY, "tipo_secundario": None, "linea": self.linea, "columna": self.columna}

    def validacion_salida_funccion(self,result:dict) -> bool:
        tipo:TipoEnum = result['tipo']
        if(self.tipo == tipo):
            tipo_secundario = result['tipo_secundario']
            if self.tipo == TipoEnum.ARRAY or self.tipo == TipoEnum.STRUCT:
                if tipo_secundario == self.tipo_secundario:
                    return True
                else:                
                    self.resultado.add_error('Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    print('Semantico', f'La funcion "{self.id}" de tipo {self.tipo.value} necesita retornar un sub tipo : {self.tipo_secundario}', self.linea, self.columna)
                    return False
            else:
                return True
        else:
            self.resultado.add_error('Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            print('Semantico', f'La funcion "{self.id}" necesita retornar un valor de tipo {self.tipo.value} y esta retornando un valor de tipo {tipo.value}', self.linea, self.columna)
            return False
    
    def graficar(self, graphviz, padre):
        graphviz.add_nodo(self.id, padre)
        graphviz.add_nodo('(', padre)
        # TODO: Agregar la imprecion de los parametros
        graphviz.add_nodo('parametros', padre)
        graphviz.add_nodo(')', padre)
        graphviz.add_nodo('{', padre)
        if (self.sentencias != None):
            self.sentencias.graficar(graphviz, padre)
        graphviz.add_nodo('}', padre)
